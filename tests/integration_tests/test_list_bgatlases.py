from pytest_bdd import scenario, when, then

from slicereg.gui.app_model import AppModel


@scenario("features/load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@when("I refresh the brainglobe atlas list")
def step_impl(model: AppModel):
    model.list_bgatlases()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(model: AppModel, bg_atlases):
    assert model.bgatlas_names == bg_atlases
