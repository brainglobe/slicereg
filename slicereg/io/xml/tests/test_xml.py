from slicereg.io.xml.reader import read_quicknii_xml
from pytest import approx

def test_xml_read_function_gets_transformation_properties_from_example_quicknii_file():
    output = read_quicknii_xml(filename='data/deepslice_output/results.xml')
    assert output.ox == approx(475.8982543945312)
    assert output.oy == approx(260.47747802734375)
    assert output.oz == approx(346.73419189453125)
    assert output.ux == approx(-481.19720458984375)
    assert output.uy == approx(5.9310126304626465)
    assert output.uz == approx(8.603763580322266)
    assert output.vx == approx(-21.585269927978516)
    assert output.vy == approx(-4.721147060394287)
    assert output.vz == approx(-389.2110595703125)

def test_xml_read_function_gets_image_metadata_from_example_quicknii_file():
    output = read_quicknii_xml(filename='data/deepslice_output/results.xml')
    assert output.first == 1
    assert output.last == 1
    assert output.name == "richards_7.18-1-Nissl_2015.png"
    assert output.filename == "richards_7.18-1-Nissl_2015.png"
    assert output.height == 700
    assert output.width == 700
    assert output.nr == 0

def test_xml_read_function_gets_parent_path_from_example_xml_file():
    output = read_quicknii_xml(filename='data/deepslice_output/results.xml')
    assert output.path == 'data/deepslice_output'

def test_xml_read_function_gets_full_image_path_from_example_xml_file():
    output = read_quicknii_xml(filename='data/deepslice_output/results.xml')
    assert output.image_path == 'data/deepslice_output/richards_7.18-1-Nissl_2015.png'