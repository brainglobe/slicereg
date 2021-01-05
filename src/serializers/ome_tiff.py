import tifffile
import xmltodict
from numpy import uint16

from src.core.section.models import Section
from src.core.section.base import BaseSectionSerializer


class OmeTiffSerializer(BaseSectionSerializer):

    def read(self, filename: str) -> Section:
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

    def write(self, section: Section, *args, **kwargs) -> None:
        raise NotImplementedError("OME Tiff Writing not yet added.")
