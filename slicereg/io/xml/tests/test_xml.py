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