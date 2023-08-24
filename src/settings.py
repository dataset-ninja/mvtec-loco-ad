from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "MVTec LOCO AD"
PROJECT_NAME_FULL: str = "MVTec LOCO AD: MVTec Logical Constraints Anomaly Detection"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.CC_BY_NC_SA_4_0()
APPLICATIONS: List[Union[Industry, Domain, Research]] = [
    Domain.Industrial(is_used=False),
    Research.AnomalyDetection(),
]
CATEGORY: Category = Category.Manufacturing()

CV_TASKS: List[CVTask] = [
    CVTask.InstanceSegmentation(),
    CVTask.SemanticSegmentation(),
    CVTask.ObjectDetection(),
]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.InstanceSegmentation()]

RELEASE_DATE: Optional[str] = "2021-03-23"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://www.mvtec.com/company/research/datasets/mvtec-loco"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 2049371
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/mvtec-loco-ad"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[
    Union[str, dict]
] = "https://www.mvtec.com/company/research/datasets/mvtec-loco"
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "0_nectarines_0_tangerines": [230, 25, 75],
    "0_nectarines_1_tangerine": [60, 180, 75],
    "0_nectarines_2_tangerines": [255, 225, 25],
    "0_nectarines_3_tangerines": [0, 130, 200],
    "0_nectarines_4_tangerines": [245, 130, 48],
    "1_additional_long_screw": [145, 30, 180],
    "1_additional_nut": [70, 240, 240],
    "1_additional_pushpin": [240, 50, 230],
    "1_additional_short_screw": [210, 245, 60],
    "1_additional_washer": [250, 190, 212],
    "1_missing_long_screw": [0, 128, 128],
    "1_missing_nut": [220, 190, 255],
    "1_missing_short_screw": [170, 110, 40],
    "1_missing_washer": [255, 250, 200],
    "1_nectarine_1_tangerine": [128, 0, 0],
    "1_very_short_screw": [170, 255, 195],
    "2_additional_nuts": [128, 128, 0],
    "2_additional_pushpins": [255, 215, 180],
    "2_additional_washers": [0, 0, 128],
    "2_missing_nuts": [128, 128, 128],
    "2_missing_washers": [230, 25, 75],
    "2_nectarines_1_tangerine": [60, 180, 75],
    "2_very_short_screws": [255, 225, 25],
    "3_nectarines_0_tangerines": [0, 130, 200],
    "bag_broken": [245, 130, 48],
    "box_damaged": [145, 30, 180],
    "broken": [70, 240, 240],
    "broken_cable": [240, 50, 230],
    "broken_connector": [210, 245, 60],
    "cable_color": [250, 190, 212],
    "cable_cut": [0, 128, 128],
    "cable_not_plugged": [220, 190, 255],
    "cable_too_short_T2": [170, 110, 40],
    "cable_too_short_T3": [255, 250, 200],
    "cable_too_short_T5": [128, 0, 0],
    "color": [170, 255, 195],
    "compartments_swapped": [128, 128, 0],
    "contamination": [255, 215, 180],
    "damaged_label": [0, 0, 128],
    "empty_bottle": [128, 128, 128],
    "extra_cable": [230, 25, 75],
    "flipped_connector": [60, 180, 75],
    "front_bent": [255, 225, 25],
    "fruit_damaged": [0, 130, 200],
    "incomplete_fruit_icon": [245, 130, 48],
    "juice_color": [145, 30, 180],
    "label_text_incomplete": [70, 240, 240],
    "misplaced_fruit_icon": [240, 50, 230],
    "misplaced_label_bottom": [230, 25, 75],
    "misplaced_label_top": [60, 180, 75],
    "missing_almonds": [255, 225, 25],
    "missing_bananas": [0, 130, 200],
    "missing_bottom_label": [245, 130, 48],
    "missing_cable": [145, 30, 180],
    "missing_cereals": [70, 240, 240],
    "missing_cereals_and_toppings": [240, 50, 230],
    "missing_connector": [210, 245, 60],
    "missing_connector_and_cable": [250, 190, 212],
    "missing_fruit_icon": [0, 128, 128],
    "missing_pushpin": [220, 190, 255],
    "missing_separator": [170, 110, 40],
    "missing_top_label": [255, 250, 200],
    "missing_toppings": [128, 0, 0],
    "mixed_cereals": [170, 255, 195],
    "open_lever": [128, 128, 0],
    "overflow": [255, 215, 180],
    "part_broken": [0, 0, 128],
    "rotated_label": [128, 128, 128],
    "screw_too_long": [230, 25, 75],
    "screw_too_short": [60, 180, 75],
    "swapped_labels": [255, 225, 25],
    "toppings_crushed": [0, 130, 200],
    "underflow": [245, 130, 48],
    "unknown_cable_color": [145, 30, 180],
    "unknown_fruit_icon": [70, 240, 240],
    "wrong_cable_location": [240, 50, 230],
    "wrong_connector_type_3_2": [210, 245, 60],
    "wrong_connector_type_5_2": [250, 190, 212],
    "wrong_connector_type_5_3": [0, 128, 128],
    "wrong_fill_level_not_enough": [220, 190, 255],
    "wrong_fill_level_too_much": [170, 110, 40],
    "wrong_juice_type": [255, 250, 200],
    "wrong_ratio": [128, 0, 0],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
PAPER: Optional[
    Union[str, List[str]]
] = "https://link.springer.com/article/10.1007/s11263-022-01578-9"
CITATION_URL: Optional[str] = "https://www.mvtec.com/company/research/datasets/mvtec-loco"
AUTHORS: Optional[List[str]] = [
    "Paul Bergmann",
    "Kilian Batzner",
    "Michael Fauser",
    "David Sattlegger",
    "Carsten Steger",
]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = "MVTec Software GmbH, Germany"
ORGANIZATION_URL: Optional[Union[str, List[str]]] = "http://www.mvtec.com/"

SLYTAGSPLIT: Optional[Dict[str, List[str]]] = None
TAGS: Optional[List[str]] = None

SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = ["test"]

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "license": LICENSE,
        "hide_dataset": HIDE_DATASET,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["project_name_full"] = PROJECT_NAME_FULL or PROJECT_NAME
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings
