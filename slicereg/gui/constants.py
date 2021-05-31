from enum import Enum, auto


class AtlasOrientation(Enum):
    CORONAL = auto()
    AXIAL = auto()
    SAGITTAL = auto()


class VolumeType(Enum):
    REGISTRATION = auto()
    ANNOTATION = auto()
