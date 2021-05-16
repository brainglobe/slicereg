import tifffile
from numpy import uint16

from slicereg.commands.base import BaseLocalImageReader, ImageReaderData


class TiffImageReader(BaseLocalImageReader):

    def read(self, filename: str) -> ImageReaderData:
        f = tifffile.TiffFile(filename)
        image = f.asarray()
        image = image.swapaxes(0,2)
        image = image.swapaxes(1,2)
        assert image.ndim == 3
        assert image.dtype == uint16

        return ImageReaderData(channels=image, resolution_um=None)


