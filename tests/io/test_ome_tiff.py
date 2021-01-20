import numpy as np
import pytest
from pytest import approx

from slicereg.io.ome_tiff import OmeTiffReader

cases = [
    ("data/RA_10X_scans/MeA/S1_09032020.ome.tiff", (2, 2816, 4198), 2.77)
]
@pytest.mark.parametrize("filename,shape,res", cases)
def test_tiff_reader_gets_sliceimages_from_example_files(filename, shape, res):
    slice_image = OmeTiffReader().read(filename=filename)
    assert slice_image.channels.ndim == 3
    assert slice_image.channels.shape == shape
    assert not np.any(np.isnan(slice_image.channels))
    assert slice_image.pixel_resolution_um == approx(res, abs=1e-2)