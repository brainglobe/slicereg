from enum import Enum, auto


class Axis(Enum):
    X = 'x'
    Y = 'y'
    Z = 'z'


class AtlasAxis(Enum):
    CORONAL = auto()
    AXIAL = auto()
    SAGITTAL = auto()
