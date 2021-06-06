from enum import Enum, auto


class Axis(Enum):
    Longitudinal = auto()
    Anteroposterior = auto()
    Horizontal = auto()


class AtlasAxis(Enum):
    CORONAL = auto()
    AXIAL = auto()
    SAGITTAL = auto()


class Direction(Enum):
    Superior = auto()
    Inferior = auto()
    Anterior = auto()
    Posterior = auto()
    Right = auto()
    Left = auto()
