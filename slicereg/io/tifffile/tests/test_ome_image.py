from _pytest.python_api import approx

from slicereg.io.tifffile.ome_image import OmeTiffImageReader


# @pytest.mark.skip(reason="If data not present, should be skipped.")
def test_ometiff_reader_gets_channels_from_example_files():
    filename = "data/RA_10X_scans/MeA/S1_09032020.ome.tiff"
    shape = (2, 2816, 4198)
    image = OmeTiffImageReader().read(filename=filename)
    assert image.channels.shape == shape


# @pytest.mark.skip(reason="If data not present, should be skipped.")
def test_ometiff_reader_gets_resolution_from_example_files():
    filename = "data/RA_10X_scans/MeA/S1_09032020.ome.tiff"
    resolution = 2.77
    image = OmeTiffImageReader().read(filename=filename)
    assert image.resolution_um == approx(resolution, abs=1e-2)
