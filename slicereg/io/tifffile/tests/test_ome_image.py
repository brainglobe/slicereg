import numpy as np
import pytest
from _pytest.python_api import approx

from slicereg.io.tifffile.ome_image import OmeTiffImageReader

cases = [
    ("data/RA_10X_scans/MeA/S1_09032020.ome.tiff", (2, 2816, 4198))
]


# @pytest.mark.skip(reason="If data not present, should be skipped.")
@pytest.mark.parametrize("filename,shape", cases)
def test_ometiff_reader_gets_channels_from_example_files(filename, shape):
    image = OmeTiffImageReader().read(filename=filename)
    assert image.channels.shape == shape


cases = [
    ("data/RA_10X_scans/MeA/S1_09032020.ome.tiff", 2.77)
]
# @pytest.mark.skip(reason="If data not present, should be skipped.")
@pytest.mark.parametrize("filename,resolution", cases)
def test_ometiff_reader_gets_resolution_from_example_files(filename, resolution):
    image = OmeTiffImageReader().read(filename=filename)
    assert image.resolution_um == approx(resolution, abs=1e-2)