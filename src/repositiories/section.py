from typing import Optional

import tifffile
import xmltodict
from numpy import uint16

from src.use_cases.base import BaseSectionRepo
from src.domain.section import Section


class InMemorySectionRepo(BaseSectionRepo):

    def __init__(self):
        self.section: Optional[Section] = None

    def get_section(self) -> Optional[Section]:
        return self.section

    def save_section(self, section: Section) -> None:
        self.section = section


def read_ome_tiff(filename: str) -> Section:
    f = tifffile.TiffFile(filename)
    image = f.asarray()
    assert image.ndim == 3
    assert image.dtype == uint16

    metadata = xmltodict.parse(f.ome_metadata)
    pix_mdata = metadata['OME']['Image']['Pixels']
    res_x, res_y = pix_mdata['@PhysicalSizeX'], pix_mdata['@PhysicalSizeY']
    assert res_x == res_y, \
        "Pixels are not square"

    return Section(channels=image, pixel_res_um=float(res_x))
