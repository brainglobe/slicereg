from numpy.testing import assert_almost_equal
from pytest_bdd import scenario, given, when, then

from slicereg.app.app_model import AppModel


@scenario("features/multichannel.feature", "Switch Channels")
def test_impl():
    ...


@given("I have loaded an image with 2 channels")
def step_impl(sidebar, model: AppModel):
    sidebar.submit_load_section_from_file("test.ome.tiff")
    assert model.num_channels == 2


@given("I am viewing channel 1")
def step_impl(model: AppModel, channels):
    assert model.current_channel == 1
    assert_almost_equal(model.section_image, channels[0])


@when("I ask for channel 2")
def step_impl(volume_view, model: AppModel):
    volume_view.press_key('2')


@then("the onscreen section data changes to channel 2")
def step_impl(model: AppModel, channels):
    assert model.current_channel == 2
    assert_almost_equal(model.section_image, channels[1])
