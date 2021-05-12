from typing import Optional

import numpy as np
import tifffile
import xmltodict
from numpy import uint16

from slicereg.commands.base import BaseImageReader
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


class OmeTiffImageReader(BaseImageReader):

    def read(self, filename: str, resolution: Optional[float] = None) -> Image:
        f = tifffile.TiffFile(filename)
        array = self._read_array(f=f)
        resolution_um = self._read_resolution(f=f) if resolution is None else resolution
        return Image(channels=array, resolution_um=resolution_um)

    @staticmethod
    def _read_array(f: tifffile.TiffFile) -> np.ndarray:
        image = f.asarray()
        assert image.ndim == 3
        assert image.dtype == uint16
        return image

    @staticmethod
    def _read_resolution(f: tifffile.TiffFile) -> float:
        metadata = xmltodict.parse(f.ome_metadata)
        pix_mdata = metadata['OME']['Image']['Pixels']
        res_x, res_y = pix_mdata['@PhysicalSizeX'], pix_mdata['@PhysicalSizeY']
        assert res_x == res_y, \
            "Pixels are not square"
        return float(res_x)