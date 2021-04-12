from pathlib import Path
from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas_from_file import LoadImioAtlasCommand
from slicereg.commands.utils import Signal
from slicereg.io.imio import ImioAtlasReader
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def command():
    repo = AtlasRepo()
    reader = Mock(ImioAtlasReader)
    return LoadImioAtlasCommand(_repo=repo, _reader=reader, atlas_updated=Mock(Signal))


@scenario("load_imio_atlas.feature", "Load Atlas From File Using imio")
def test_outlined():
    ...


@given("A file containing an atlas")
def check_file_exists(command):
    command._reader.read.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=10)


@when("I load the mock.tiff atlas with 10um resolution")
def load_atlas(command):
    command(filename='mock.tiff', resolution_um=10)


@then("a 3D volume of the atlas appears onscreen")
def check_3d_atlas_data_shown(command, filename):
    output = command.atlas_updated.emit.call_args[1]
    assert output['volume'].ndim == 3
    assert output['transform'].shape == (4, 4)
    command._repo.load_atlas_from_file.assert_called_with(filename=filename)


@then("it is set as the current atlas for the session")
def check_atlas_set_in_repo(command):
    assert command._repo.get_atlas().resolution_um == 10
