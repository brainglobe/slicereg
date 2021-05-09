from pathlib import Path
from unittest.mock import Mock

import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.commands.load_atlas import LoadAtlasFromFileCommand
from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.imio import ImioAtlasReader
from slicereg.models.atlas import Atlas
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def model():
    reader = Mock(ImioAtlasReader)
    reader.read.return_value = Atlas(volume=random.normal(size=(4, 4, 4)), resolution_um=10)
    commands = Mock(CommandProvider)
    commands.load_atlas_from_file = LoadAtlasFromFileCommand(_repo=AtlasRepo(), _reader=reader)
    model = AppModel(_commands=commands)
    return model


@scenario("load_atlas.feature", "Load Atlas From File Using imio")
def test_outlined():
    ...


@when("I load the mock.tiff atlas with 10um resolution")
def load_atlas(model):
    model.load_atlas_from_file(filename='mock.tiff', resolution_um=10)


@then("a 3D volume of the atlas appears onscreen")
def check_3d_atlas_data_shown(model):
    assert model.atlas_volume.ndim == 3
    assert model.atlas_resolution == 10
