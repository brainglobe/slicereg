from pathlib import Path
from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas_from_file import LoadAtlasFromFileCommand
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def filename():
    fn = Mock(Path('mock_atlas.nii'))
    fn.exists.return_value = True
    return fn


@pytest.fixture
def command():
    repo = Mock(AtlasRepo)
    repo.load_atlas_from_file.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=25)
    return LoadAtlasFromFileCommand(_repo=repo, atlas_updated=Mock(Signal))


@scenario("load_atlas_from_file.feature", "Load Atlas From NII File")
def test_outlined():
    ...


@given("A file containing an atlas")
def check_file_exists(filename):
    assert filename.exists()


@when("I load the atlas NII file")
def load_atlas(command, filename):
    command(filename)


@then("a 3D volume of the atlas appears onscreen")
def check_3d_atlas_data_shown(command, filename):
    output = command.atlas_updated.emit.call_args[1]
    assert output['volume'].ndim == 3
    assert output['transform'].shape == (4, 4)
    command._repo.load_atlas_from_file.assert_called_with(filename=filename)


@then("it is set as the current atlas for the session")
def check_atlas_set_in_repo(command):
    assert command._repo.set_atlas.call_count == 1
