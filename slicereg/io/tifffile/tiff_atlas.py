import tifffile as tif

from slicereg.core.atlas import Atlas


class TifffileAtlasReader:

    @staticmethod
    def read(filename: str, resolution_um: int) -> Atlas:
        return Atlas(volume=tif.imread(filename), resolution_um=resolution_um)


