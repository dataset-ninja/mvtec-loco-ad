import os
import shutil
from urllib.parse import unquote, urlparse

import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import dir_exists, file_exists, get_file_ext, get_file_name
from supervisely.io.json import load_json_file
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(desc=f"Downloading '{file_name_with_ext}' to buffer...", total=fsize) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/MVTEC LOCO AD/mvtec_loco_anomaly_detection"
    batch_size = 30
    bbox_suffix = "_bbox"

    train_images_pathes = "train/good"
    val_images_pathes = "validation/good"
    test_images_pathes = "test"
    masks_pathes = "ground_truth"
    classes_json = "defects_config.json"

    def create_ann_train_val(image_path, images_type):
        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        tag = sly.Tag(meta=image_type_to_tag[images_type])

        return sly.Annotation(img_size=(img_height, img_wight), labels=[], img_tags=[tag])

    def create_ann_test(image_path):
        labels = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]
        if good_subfolder is False:
            mask_folder_name = get_file_name(image_path)
            curr_masks_path = os.path.join(masks_path, curr_subfolder_name, mask_folder_name)
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

        tag = sly.Tag(meta=subfolder_to_tag[curr_subfolder_name])
        tag_test = sly.Tag(meta=tag_meta_test)

        return sly.Annotation(
            img_size=(img_height, img_wight), labels=labels, img_tags=[tag, tag_test]
        )

    tag_meta_train = sly.TagMeta("train", sly.TagValueType.NONE)
    tag_meta_val = sly.TagMeta("validation", sly.TagValueType.NONE)
    tag_meta_test = sly.TagMeta("test", sly.TagValueType.NONE)
    tag_logical_anomalies = sly.TagMeta("logical_anomalies", sly.TagValueType.NONE)
    tag_structural_anomalies = sly.TagMeta("structural_anomalies", sly.TagValueType.NONE)
    tag_good = sly.TagMeta("good", sly.TagValueType.NONE)
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

    image_type_to_tag = {"train": tag_meta_train, "validation": tag_meta_val}
    subfolder_to_tag = {
        "logical_anomalies": tag_logical_anomalies,
        "structural_anomalies": tag_structural_anomalies,
        "good": tag_good,
    }

    all_datasets = os.listdir(dataset_path)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        tag_metas=[
            tag_meta_train,
            tag_meta_val,
            tag_meta_test,
            tag_logical_anomalies,
            tag_structural_anomalies,
            tag_saturation_threshold,
            tag_relative_saturation,
            tag_good,
        ]
    )
    api.project.update_meta(project.id, meta.to_json())

    for curr_dataset in all_datasets:
        ds_path = os.path.join(dataset_path, curr_dataset)
        if dir_exists(ds_path):
            dataset = api.dataset.create(project.id, curr_dataset, change_name_if_conflict=True)

            train_images_path = os.path.join(ds_path, train_images_pathes)
            val_images_path = os.path.join(ds_path, val_images_pathes)
            for curr_path in [train_images_path, val_images_path]:
                images_type = curr_path.split("/")[-2]
                curr_images_names = os.listdir(curr_path)
                progress = sly.Progress(
                    "Create dataset {}, add {} images".format(curr_dataset, images_type),
                    len(curr_images_names),
                )

                for img_names_batch in sly.batched(curr_images_names, batch_size=batch_size):
                    images_pathes_batch = [
                        os.path.join(train_images_path, image_name)
                        for image_name in img_names_batch
                    ]

                    new_images_names_batch = [
                        get_file_name(name) + "_ " + images_type + get_file_ext(name)
                        for name in img_names_batch
                    ]

                    img_infos = api.image.upload_paths(
                        dataset.id, new_images_names_batch, images_pathes_batch
                    )
                    img_ids = [im_info.id for im_info in img_infos]
                    anns_batch = [
                        create_ann_train_val(image_path, images_type)
                        for image_path in images_pathes_batch
                    ]
                    api.annotation.upload_anns(img_ids, anns_batch)

                    progress.iters_done_report(len(img_names_batch))

            test_image_path = os.path.join(ds_path, test_images_pathes)
            masks_path = os.path.join(ds_path, masks_pathes)
            defects_json_path = os.path.join(ds_path, classes_json)

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
            api.project.update_meta(project.id, meta.to_json())

            good_subfolder = False
            for curr_subfolder_name in os.listdir(test_image_path):
                if curr_subfolder_name == "good":
                    good_subfolder = True
                curr_test_images_path = os.path.join(test_image_path, curr_subfolder_name)
                curr_test_images_names = os.listdir(curr_test_images_path)
                progress = sly.Progress(
                    "Create dataset {}, add test images, subfolder {}".format(
                        curr_dataset, curr_subfolder_name
                    ),
                    len(curr_test_images_names),
                )

                for img_names_batch in sly.batched(curr_test_images_names, batch_size=batch_size):
                    images_pathes_batch = [
                        os.path.join(curr_test_images_path, image_name)
                        for image_name in img_names_batch
                    ]

                    new_img_names_batch = [
                        get_file_name(image_name)
                        + "_test_"
                        + curr_subfolder_name
                        + get_file_ext(image_name)
                        for image_name in img_names_batch
                    ]

                    img_infos = api.image.upload_paths(
                        dataset.id, new_img_names_batch, images_pathes_batch
                    )
                    img_ids = [im_info.id for im_info in img_infos]

                    anns_batch = [create_ann_test(image_path) for image_path in images_pathes_batch]
                    api.annotation.upload_anns(img_ids, anns_batch)

                    progress.iters_done_report(len(img_names_batch))

    return project
