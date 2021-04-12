import numpy as np
import pytest
from pytest import approx

from slicereg.io.tifffile import OmeTiffSectionReader

cases = [
    ("data/RA_10X_scans/MeA/S1_09032020.ome.tiff", (2, 2816, 4198), 2.77)
]
@pytest.mark.parametrize("filename,shape,pixel_size_um", cases)
def test_tiff_reader_gets_sliceimages_from_example_files(filename, shape, pixel_size_um):
    section = OmeTiffSectionReader().read(filename=filename)

    assert section.image.num_channels == shape[0]
    assert section.image.height == shape[1]
    assert section.image.width == shape[2]
    assert not np.any(np.isnan(section.image.channels))
    assert section.pixel_resolution_um == approx(pixel_size_um, abs=1e-2)
