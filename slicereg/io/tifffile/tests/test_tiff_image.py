from slicereg.io.tifffile.tiff_image import TiffImageReader


# @pytest.mark.skip(reason="If data not present, should be skipped.")
def test_tiff_reader_gets_sliceimages_from_example_file():
    filename = "data/cortexlab_data/richards_7.18.tif"
    shape = (3, 801, 1140)
    image = TiffImageReader().read(filename=filename)
    assert image.channels.shape == shape


