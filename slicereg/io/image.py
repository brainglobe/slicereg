from pathlib import Path

from slicereg.commands.base import BaseLocalImageReader, ImageReaderData
from slicereg.io.tifffile.ome_image import OmeTiffImageReader
from slicereg.io.tifffile.tiff_image import TiffImageReader


class ImageReader(BaseLocalImageReader):

    def read(self, filename: str,) -> ImageReaderData:
        filepath = Path(filename)
        if '.ome' in filepath.suffixes:
            return OmeTiffImageReader().read(filename=str(filepath))
        elif filepath.suffix.lower() in ['.tiff', '.tif']:
            return TiffImageReader().read(filename=str(filepath))
        else:
            raise TypeError(f"{filepath.suffix} not supported.")

