import tifffile
import tifffile as tif
import xmltodict
from numpy import uint16

from slicereg.models.atlas import Atlas
from slicereg.models.image import Image


class TifffileAtlasReader:

    @staticmethod
    def read(path: str, resolution_um: int) -> Atlas:
        return Atlas(volume=tif.imread(path), resolution_um=resolution_um)


class OmeTiffImageReader:

    def read(self, filename: str) -> Image:
        f = tifffile.TiffFile(filename)
        image = f.asarray()
        assert image.ndim == 3
        assert image.dtype == uint16

        metadata = xmltodict.parse(f.ome_metadata)
        pix_mdata = metadata['OME']['Image']['Pixels']
        res_x, res_y = pix_mdata['@PhysicalSizeX'], pix_mdata['@PhysicalSizeY']
        assert res_x == res_y, \
            "Pixels are not square"

        return Image(channels=image, resolution_um=float(res_x))
