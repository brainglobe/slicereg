from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_section import BaseSectionRepo, LoadImageCommand, BaseSectionReader
from slicereg.gui.view_model import ViewModel, LoadSectionPresenter
from slicereg.models.section import SliceImage


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = []
    return repo


@pytest.fixture
def view_model():
    return ViewModel()


@pytest.fixture
def image_data():
    return np.arange(12).reshape((2, 3, 2))


@pytest.fixture
def reader(image_data):
    reader = Mock(BaseSectionReader)
    reader.read.return_value = SliceImage(channels=image_data, pixel_resolution_um=10)
    return reader


@pytest.fixture
def command(repo, reader, view_model):
    return LoadImageCommand(repo=repo, presenter=LoadSectionPresenter(view_model=view_model),
                             reader=reader)


@scenario("load_slice.feature", "Single Slice Import")
def test_outlined():
    ...


@given("I have a multichannel OME-TIFF file on my computer.", target_fixture="filename")
def filename():
    return 'a_real_file.ome.tiff'


@given("No sections have been loaded yet")
def no_sections_loaded(repo, view_model):
    assert not repo.sections
    assert not view_model.current_section


@when("I load the file")
def load_file(command, filename):
    command(filename=filename)


@then("I should see the slice image onscreen in 3D")
def check_for_loaded_3d_section(view_model, image_data):
    assert view_model.current_section
    assert view_model.current_section.transform.shape == (4, 4)
