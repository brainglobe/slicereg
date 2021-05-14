import numpy as np
from pytest import approx

from slicereg.io.tifffile.tiff_image import TiffImageReader


# @pytest.mark.skip(reason="If data not present, should be skipped.")
def test_tiff_reader_gets_sliceimages_from_example_file():
    filename = "data/cortexlab_data/richards_7.18.tif"
    resolution_um = 10.
    shape = (3, 801, 1140)
    image = TiffImageReader().read(filename=filename, resolution_um=resolution_um)
    
    assert image.num_channels == shape[0]
    assert image.height == shape[1]
    assert image.width == shape[2]
    assert not np.any(np.isnan(image.channels))
    assert image.resolution_um == approx(resolution_um, abs=1e-2)
    

