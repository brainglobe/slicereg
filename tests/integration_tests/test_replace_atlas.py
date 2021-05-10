import numpy.testing as npt
from pytest_bdd import scenario, given, when, then


@scenario("features/load_atlas.feature", "Replace Atlas")
def test_outlined():
    ...


@given("the 25um atlas is currently loaded")
def load_first_atlas(model, atlas_volume):
    model.load_bgatlas("first_atlas")
    assert model.atlas_resolution == 25
    npt.assert_almost_equal(model.atlas_volume, atlas_volume)


@when("I ask for a 100um atlas")
def load_second_atlas(model):
    model.load_bgatlas(name="allen_mouse_100um")


@then("a 3D volume of the 100um allen reference atlas appears.")
def check_3d_atlas_data_shown(model, second_volume):
    assert model.atlas_resolution == 100
    npt.assert_almost_equal(model.atlas_volume, second_volume)
