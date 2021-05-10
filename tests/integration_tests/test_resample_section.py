from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/resample.feature", "Section Resample")
def test_impl():
    ...


@given("I have a 10um-resolution section loaded")
def step_impl(model: AppModel):
    model.load_section("test.ome.tiff")
    assert model.section_image_resolution == 10
    assert model.section_image.shape == (3, 4)


@when("I set the resolution to 50um")
def step_impl(model: AppModel):
    model.resample_section(resolution_um=50)


@then("I should see a 50um resolution slice onscreen")
def step_impl(model: AppModel):
    assert model.section_image_resolution == 50
    assert model.section_image.shape == (1, 1)
