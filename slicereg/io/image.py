from pathlib import Path
from typing import Optional

from slicereg.commands.base import BaseLocalImageReader
from slicereg.core.image import Image
from slicereg.io.tifffile.tiff_image import TiffImageReader
from slicereg.io.tifffile.ome_image import OmeTiffImageReader


class ImageReader(BaseLocalImageReader):

    def read(self, filename: str, resolution: Optional[float]) -> Image:
        filepath = Path(filename)
        if '.ome' in filepath.suffixes:
            return OmeTiffImageReader().read(filename=str(filepath))
        elif filepath.suffix.lower() in ['.tiff', '.tif']:
            return TiffImageReader().read(filename=str(filepath), resolution_um=10)
        else:
            raise TypeError(f"{filepath.suffix} not supported.")

