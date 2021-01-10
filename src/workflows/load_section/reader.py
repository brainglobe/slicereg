import tifffile
import xmltodict
from numpy import uint16

from src.workflows.load_section.load_section import BaseSectionReader
from src.models.section import Section


class OmeTiffReader(BaseSectionReader):

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
