from slicereg.models.section import Section, ImageData
from slicereg.models.atlas import Atlas
from copy import copy

def register(section: Section, atlas: Atlas) -> Section:
    return Section(
        image=copy(section.image),
        plane_2d=copy(section.plane_2d),
        plane_3d=copy(section.plane_3d),
    )