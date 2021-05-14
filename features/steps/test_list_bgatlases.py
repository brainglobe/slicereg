from pytest_bdd import scenario, when, then


@scenario("../load_atlas.feature", "List Available Brainglobe Atlases")
def test_outlined():
    ...


@when("I refresh the brainglobe atlas list")
def step_impl(sidebar):
    sidebar.click_update_bgatlas_list_button()


@then("I see a list of bg-atlasapi's available atlases.")
def step_impl(sidebar, bg_atlases):
    sidebar.bgatlas_dropdown_entries == bg_atlases
