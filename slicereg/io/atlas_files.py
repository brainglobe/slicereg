import imio

from slicereg.models.atlas import Atlas
import tifffile as tif


def load_atlas_from_file(tiff_stack_filename: str, resolution: float) -> Atlas:
    return Atlas(volume=tif.imread(tiff_stack_filename), resolution_um=resolution)


def load_atlas_from_file2(filename: str) -> Atlas:
    # TODO: can support scaling, parallel loading, map to coordinate space (anterior, left, superior, etc.)
    volume = imio.load_any(filename)

    # TODO: resolution
    return Atlas(
        volume=volume,
        resolution_um=60,
    )
