import glob
import os

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
)
from supervisely.io.json import load_json_file


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # https://www.mvtec.com/company/research/datasets/mvtec-loco/downloads

    # if sly.is_development():
    # load_dotenv("local.env")
    # load_dotenv(os.path.expanduser("~/supervisely.env"))

    # api = sly.Api.from_env()
    # team_id = sly.env.team_id()
    # workspace_id = sly.env.workspace_id()

    # project_name = "MVTEC LOCO AD"
    dataset_path = "APP_DATA/mvtec_loco_anomaly_detection"
    batch_size = 30
    bbox_suffix = "_bbox"

    train_images_pathes = "train/good"
    val_images_pathes = "validation/good"
    test_images_pathes = "test"
    masks_pathes = "ground_truth"
    classes_json = "defects_config.json"

    def create_ann(image_path):
        labels = []
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        class_name = image_path.split("/")[-4]
        subfolder_name = image_path.split("/")[-2]

        tag_class_meta = class_folder_to_tag[class_name]
        tag_class = sly.Tag(tag_class_meta)

        tag_subfolder_meta = subfolder_to_tag[subfolder_name]
        tag_subfolder = sly.Tag(tag_subfolder_meta)

        if curr_dataset == "test" and subfolder_name != "good":
            curr_masks_path = (
                image_path.split(curr_dataset)[0]
                + "ground_truth/"
                + subfolder_name
                + "/"
                + get_file_name(image_path)
            )
            pixel_to_defect_data = json_anns_to_sub_ds[class_name]
            for mask_name in os.listdir(curr_masks_path):
                mask_path = os.path.join(curr_masks_path, mask_name)
                if file_exists(mask_path):
                    mask_np = sly.imaging.image.read(mask_path)[:, :, 0]
                    unique_pixels = np.unique(mask_np)
                    if len(unique_pixels) > 1:
                        for pixel in unique_pixels[1:]:
                            curr_ann_data = pixel_to_defect_data.get(pixel)
                            if curr_ann_data is not None:
                                obj_class = curr_ann_data[0]
                                mask = mask_np == pixel
                                ret, curr_mask = connectedComponents(
                                    mask.astype("uint8"), connectivity=8
                                )
                                for i in range(1, ret):
                                    obj_mask = curr_mask == i
                                    curr_bitmap = sly.Bitmap(obj_mask)
                                    if curr_bitmap.area > 50:
                                        tag_threshold = sly.Tag(
                                            tag_saturation_threshold, curr_ann_data[1]
                                        )
                                        tag_relative = sly.Tag(
                                            tag_relative_saturation, str(curr_ann_data[2])
                                        )
                                        curr_label = sly.Label(
                                            curr_bitmap,
                                            obj_class,
                                            tags=[tag_threshold, tag_relative],
                                        )
                                        labels.append(curr_label)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[tag_class, tag_subfolder]
        )

    tag_logical_anomalies = sly.TagMeta("logical_anomaly", sly.TagValueType.NONE)
    tag_structural_anomalies = sly.TagMeta("structural_anomaly", sly.TagValueType.NONE)
    tag_good = sly.TagMeta("good", sly.TagValueType.NONE)

    tag_breakfast_box = sly.TagMeta("breakfast_box", sly.TagValueType.NONE)
    tag_juice_bottle = sly.TagMeta("juice_bottle", sly.TagValueType.NONE)
    tag_pushpins = sly.TagMeta("pushpins", sly.TagValueType.NONE)
    tag_screw_bag = sly.TagMeta("screw_bag", sly.TagValueType.NONE)
    tag_splicing_connectors = sly.TagMeta("splicing_connectors", sly.TagValueType.NONE)

    tag_saturation_threshold = sly.TagMeta(
        "saturation_threshold",
        sly.TagValueType.ANY_NUMBER,
        applicable_to=sly.TagApplicableTo.OBJECTS_ONLY,
    )
    tag_relative_saturation = sly.TagMeta(
        "relative_saturation",
        sly.TagValueType.ONEOF_STRING,
        possible_values=["True", "False"],
        applicable_to=sly.TagApplicableTo.OBJECTS_ONLY,
    )

    subfolder_to_tag = {
        "logical_anomalies": tag_logical_anomalies,
        "structural_anomalies": tag_structural_anomalies,
        "good": tag_good,
    }

    class_folder_to_tag = {
        "breakfast_box": tag_breakfast_box,
        "juice_bottle": tag_juice_bottle,
        "pushpins": tag_pushpins,
        "screw_bag": tag_screw_bag,
        "splicing_connectors": tag_splicing_connectors,
    }

    all_datasets = os.listdir(dataset_path)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        tag_metas=[
            tag_logical_anomalies,
            tag_structural_anomalies,
            tag_saturation_threshold,
            tag_relative_saturation,
            tag_good,
            tag_breakfast_box,
            tag_juice_bottle,
            tag_pushpins,
            tag_screw_bag,
            tag_splicing_connectors,
        ]
    )
    api.project.update_meta(project.id, meta.to_json())

    all_train_images = glob.glob(dataset_path + "/*/train/good/*.png")
    all_val_images = glob.glob(dataset_path + "/*/validation/good/*.png")
    all_test_images = glob.glob(dataset_path + "/*/test/*/*.png")
    all_test_masks = glob.glob(dataset_path + "/*/ground_truth/*/*/*.png")

    ds_name_to_data_pathes = {
        "test": all_test_images,
        "train": all_train_images,
        "validation": all_val_images,
    }

    json_anns_to_sub_ds = {}
    all_json_data_pathes = glob.glob(dataset_path + "/*/defects_config.json")
    for defects_json_path in all_json_data_pathes:
        defects_data = load_json_file(defects_json_path)
        pixel_to_defect_data = {}
        for curr_defect_data in defects_data:
            class_exist = meta.get_obj_class(curr_defect_data["defect_name"])
            if class_exist is not None:
                defect_obj_class = class_exist
            else:
                defect_obj_class = sly.ObjClass(curr_defect_data["defect_name"], sly.Bitmap)
                meta = meta.add_obj_class(defect_obj_class)
            pixel_to_defect_data[curr_defect_data["pixel_value"]] = (
                defect_obj_class,
                curr_defect_data["saturation_threshold"],
                curr_defect_data["relative_saturation"],
            )
            json_anns_to_sub_ds[defects_json_path.split("/")[-2]] = pixel_to_defect_data
        api.project.update_meta(project.id, meta.to_json())

    for curr_dataset in list(ds_name_to_data_pathes.keys()):
        dataset = api.dataset.create(project.id, curr_dataset, change_name_if_conflict=True)
        images_pathes = ds_name_to_data_pathes[curr_dataset]

        progress = sly.Progress("Create dataset {}".format(curr_dataset), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            if curr_dataset == "test":
                img_names_batch = [
                    im_path.split("/")[-4]
                    + "_"
                    + im_path.split("/")[-2]
                    + "_"
                    + get_file_name_with_ext(im_path)
                    for im_path in img_pathes_batch
                ]
            else:
                img_names_batch = [
                    im_path.split("/")[-4] + "_" + get_file_name_with_ext(im_path)
                    for im_path in img_pathes_batch
                ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_pathes_batch))

    return project
