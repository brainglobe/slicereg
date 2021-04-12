from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_section import BaseSectionRepo, LoadImageCommand
from slicereg.io.base import BaseSectionReader
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.models.section import Section
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = []
    return repo


@pytest.fixture
def atlas_repo():
    repo = Mock(AtlasRepo)
    repo.get_atlas.return_value = Atlas(volume=np.random.random((5, 5, 5)), resolution_um=10)
    return repo


@pytest.fixture
def image_data():
    return np.arange(12).reshape((2, 3, 2))


@pytest.fixture
def reader(image_data):
    reader = Mock(BaseSectionReader)
    reader.read.return_value = Section(Image(channels=image_data), pixel_resolution_um=10)
    return reader


@pytest.fixture
def command(repo, atlas_repo, reader):
    return LoadImageCommand(_repo=repo, _atlas_repo=atlas_repo, section_loaded=Mock(Signal), _reader=reader)


@scenario("load_slice.feature", "Single Slice Import")
def test_outlined():
    ...


@given("I have a multichannel OME-TIFF file on my computer.", target_fixture="filename")
def filename():
    return 'a_real_file.ome.tiff'


@given("No sections have been loaded yet")
def no_sections_loaded(repo):
    assert not repo.sections


@when("I load the file")
def load_file(command, filename):
    command(filename=filename)


@then("I should see the slice image onscreen in 3D")
def check_for_loaded_3d_section(command: LoadImageCommand):
    output = command.section_loaded.emit.call_args[1]
    assert output['image'].ndim == 2
    assert output['transform'].shape == (4, 4)


@then("The slice is centered on the image")
def check_the_transform_isnt_zero(command: LoadImageCommand):
    output = command.section_loaded.emit.call_args[1]
    assert output['transform'][0, -1] != 0
    assert output['transform'][1, -1] != 0


@then("The displayed resolution is set to the image's resolution")
def check_resolution_is_sent(command: LoadImageCommand):
    output = command.section_loaded.emit.call_args[1]
    assert output['resolution_um'] == 10
