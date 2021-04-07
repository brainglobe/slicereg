from slicereg.models.atlas import Atlas
import tifffile as tif


def load_atlas_from_file(tiff_stack_filename: str, resolution: float) -> Atlas:
    return Atlas(volume=tif.imread(tiff_stack_filename), resolution_um=resolution)
