from pathlib import Path
from unittest.mock import Mock

import pytest
from numpy import ndarray
from pytest_bdd import scenario, given, when, then

from slicereg.workflows.load_section import LoadImageWorkflow, OmeTiffReader
from slicereg.gui.presenters import LoadSectionPresenter
from slicereg.workflows.shared.repos.section_repo import InMemorySectionRepo


@pytest.fixture
def workflow():
    return LoadImageWorkflow(repo=InMemorySectionRepo(), presenter=Mock(LoadSectionPresenter),
                             reader=OmeTiffReader())


@scenario("load_slice.feature", "Single Slice Import")
def test_outlined():
    ...


@given("I have a multichannel OME-TIFF file on my computer.", target_fixture="filename")
def filename():
    filename = 'data/RA_10X_scans/MeA/S1_09032020.ome.tiff'
    path = Path(filename)
    assert path.exists()
    assert path.name[-9:] == ".ome.tiff"
    return filename


@given("No sections have been loaded yet")
def repo(workflow):
    assert not workflow._repo.sections


@when("I load the file")
def load_file(workflow, filename):
    workflow.execute(filename=filename, channel=1)


@then("I should see the file image onscreen in 3D")
def check_for_loaded_3d_section(workflow):
    view_model = workflow._presenter.show.call_args[0][0]  # Grab what was passed to Presenter.show()
    assert isinstance(view_model.section, ndarray)
    assert view_model.model_matrix.shape == (4, 4)
