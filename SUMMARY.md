**MVTec LOCO AD: MVTec Logical Constraints Anomaly Detection** is a dataset for instance segmentation, semantic segmentation, and object detection tasks. It is used in the industrial domain, and in the anomaly detection research. 

The dataset consists of 3651 images with 1969 labeled objects belonging to 83 different classes including *contamination*, *missing_pushpin*, *color*, and other: *1_additional_pushpin*, *fruit_damaged*, *broken*, *wrong_cable_location*, *part_broken*, *missing_top_label*, *missing_bottom_label*, *wrong_fill_level_not_enough*, *wrong_juice_type*, *damaged_label*, *screw_too_long*, *screw_too_short*, *1_very_short_screw*, *bag_broken*, *front_bent*, *juice_color*, *missing_separator*, *swapped_labels*, *empty_bottle*, *wrong_fill_level_too_much*, *missing_connector*, *missing_cable*, *extra_cable*, *cable_color*, *broken_cable*, and 55 more.

Images in the MVTec LOCO AD dataset have pixel-level instance segmentation annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation (only one mask for every class) or object detection (bounding boxes for every object) tasks. There are 2672 (73% of the total) unlabeled images (i.e. without annotations). There are 3 splits in the dataset: *test* (1568 images), *train* (1778 images), and *validation* (305 images). The dataset was released in 2021 by the MVTec Software GmbH, Germany.

Here is the visualized example grid with animated annotations:

[animated grid](https://github.com/dataset-ninja/mvtec-loco-ad/raw/main/visualizations/horizontal_grid.webm)
