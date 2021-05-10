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
    reader.read.return_value = Image(channels=np.empty((2, 3, 4)), resolution_um=12.)
    commands = CommandProvider(_section_ome_reader=reader, _atlas_repo=atlas_repo)
    model = AppModel(_commands=commands)
    return model


@scenario("features/section_affine_registration.feature", "Move Section in 3D")
def test_impl():
    ...


@given("I have loaded a section")
def step_impl(model: AppModel):
    model.load_section("test.ome.tiff")
    assert model.section_image is not None
    assert model.section_transform is not None


@when("I ask for the section to be translated and rotated")
def step_impl(model: AppModel):
    model.move_section(x=2, y=5, z=10, rx=0, ry=0, rz=0)


@then("the image is updated with a new 3D transform")
def step_impl(model: AppModel):
    assert model.section_transform is not None  # todo: figure out how to detect a change


@then("an atlas section image at that transform is shown.")
def step_impl(model: AppModel):
    assert model.section_image is not None  # todo: figure out how to detect a change

