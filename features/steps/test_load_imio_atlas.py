from pytest_bdd import scenario, when, then


@scenario("../load_atlas.feature", "Load Atlas From File Using imio")
def test_outlined():
    ...


@when("I load the mock.tiff atlas with 10um resolution")
def load_atlas(sidebar):
    sidebar.atlas_resolution_text = "10"
    sidebar.submit_load_atlas_from_file(filename='mock.tiff')


@then("a 3D volume of the atlas appears onscreen")
def check_3d_atlas_data_shown(model):
    assert model.registration_volume.ndim == 3
    assert model.atlas_resolution == 10
