from slicereg.io.xml.reader import read_quicknii_xml


def test_xml_read_function_gets_transformation_properties_from_example_quicknii_file():
    output = read_quicknii_xml(filename='data/deepslice_output/results.xml')
    assert output.ox == 475.8982543945312
    # assert output.oy == 260.47747802734375
    # assert output.oz == 346.73419189453125
    # assert output.ux == -481.19720458984375
    # assert output.uy == 5.9310126304626465
    # assert output.uz == 8.603763580322266
    # assert output.vx == -21.585269927978516
    # assert output.vy == -4.721147060394287
    # assert output.vz == -389.2110595703125