import numpy as np
import pytest
from _pytest.python_api import approx

from slicereg.io.tifffile.ome_image import OmeTiffImageReader

cases = [
    ("data/RA_10X_scans/MeA/S1_09032020.ome.tiff", (2, 2816, 4198), 2.77)
]


# @pytest.mark.skip(reason="If data not present, should be skipped.")
@pytest.mark.parametrize("filename,shape,pixel_size_um", cases)
def test_ometiff_reader_gets_sliceimages_from_example_files(filename, shape, pixel_size_um):
    image = OmeTiffImageReader().read(filename=filename)

    assert image.num_channels == shape[0]
    assert image.height == shape[1]
    assert image.width == shape[2]
    assert not np.any(np.isnan(image.channels))
    assert image.resolution_um == approx(pixel_size_um, abs=1e-2)
