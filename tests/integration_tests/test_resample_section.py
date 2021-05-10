from unittest.mock import Mock

import numpy as np
import pytest
from numpy import random
from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.tifffile import OmeTiffImageReader
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def model():
    atlas_repo = AtlasRepo()
    atlas_repo.set_atlas(Atlas(volume=random.normal(size=(10, 10, 10)), resolution_um=25))
    reader = Mock(OmeTiffImageReader)
    reader.read.return_value = Image(channels=np.empty((2, 3, 4)), resolution_um=10.)
    commands = CommandProvider(_section_ome_reader=reader, _atlas_repo=atlas_repo)
    model = AppModel(_commands=commands)
    return model


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
