from unittest.mock import Mock

import numpy as np
import pytest
from numpy import random
from numpy.testing import assert_almost_equal
from pytest_bdd import scenario, given, when, then

from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.tifffile import OmeTiffImageReader
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.repos.atlas_repo import AtlasRepo


@pytest.fixture
def channels():
    return np.empty((2, 3, 4))


@pytest.fixture
def model(channels):
    atlas_repo = AtlasRepo()
    atlas_repo.set_atlas(Atlas(volume=random.normal(size=(10, 10, 10)), resolution_um=25))
    reader = Mock(OmeTiffImageReader)
    reader.read.return_value = Image(channels=channels, resolution_um=10.)
    commands = CommandProvider(_section_ome_reader=reader, _atlas_repo=atlas_repo)
    model = AppModel(_commands=commands)
    return model


@scenario("features/multichannel.feature", "Switch Channels")
def test_impl():
    ...


@given("I have loaded an image with 2 channels")
def step_impl(model: AppModel):
    model.load_section("fake.ome.tiff")
    assert model.num_channels == 2


@given("I am viewing channel 1")
def step_impl(model: AppModel, channels):
    assert model.current_channel == 1
    assert_almost_equal(model.section_image, channels[0])


@when("I ask for channel 2")
def step_impl(model: AppModel):
    model.select_channel(2)


@then("the onscreen section data changes to channel 2")
def step_impl(model: AppModel, channels):
    assert model.current_channel == 2
    assert_almost_equal(model.section_image, channels[1])
