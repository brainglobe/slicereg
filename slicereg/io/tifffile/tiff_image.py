import tifffile
from numpy import uint16

from slicereg.core.image import Image


class TiffImageReader:

    def read(self, filename: str, resolution_um: float) -> Image:
        f = tifffile.TiffFile(filename)
        image = f.asarray()
        image = image.swapaxes(0,2)
        image = image.swapaxes(1,2)
        assert image.ndim == 3
        assert image.dtype == uint16

        return Image(channels=image, resolution_um=resolution_um)


