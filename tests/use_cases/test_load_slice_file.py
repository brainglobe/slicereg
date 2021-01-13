from pathlib import Path

from numpy import ndarray
from pytest_bdd import scenario, given, when, then

from slicereg.workflows.load_section import LoadImageWorkflow, OmeTiffReader
from slicereg.workflows.load_section.view_model import LoadImageViewModel, LoadImagePresenter
from slicereg.workflows.shared.repos.section_repo import InMemorySectionRepo


@scenario("features/load_slice.feature", "Single Slice Import")
def test_outlined():
    ...


@given("I have a multichannel OME-TIFF file on my computer.", target_fixture="filename")
def filename():
    filename = 'data/RA_10X_scans/MeA/S1_09032020.ome.tiff'
    path = Path(filename)
    assert path.exists()
    assert path.name[-9:] == ".ome.tiff"
    return filename


@given("No sections have been loaded yet", target_fixture="repo")
def repo():
    repo = InMemorySectionRepo()
    assert not repo.sections
    return repo


@given("No sections are onscreen", target_fixture="view_model")
def view_model():
    model = LoadImageViewModel()
    assert not model.sections
    return model


@when("I load the file")
def load_file(filename, repo, view_model):
    workflow = LoadImageWorkflow(repo=repo, presenter=LoadImagePresenter(model=view_model), reader=OmeTiffReader())
    workflow.execute(filename=filename)


@then("I should see the file image onscreen")
def check_for_loaded_section(view_model):
    assert len(view_model.sections) == 1


@then("it should have some default 3D transformation.")
def check_metadata(view_model):
    assert isinstance(view_model.sections[0].model_matrix, ndarray)
    assert view_model.sections[0].model_matrix.shape == (4, 4)
