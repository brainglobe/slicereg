from dataclasses import dataclass

import numpy as np



@dataclass
class Atlas:
    registration_volume  # 3dim array of intensities
    annotation_id_volume # 3dim array of usually
    annotation_labels # dataframe with id (int), region_name (str), group_level (int), sometimes parent_id (int)