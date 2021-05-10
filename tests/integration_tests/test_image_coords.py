from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then

from slicereg.commands.base import BaseSectionRepo
from slicereg.commands.get_coords import MapImageCoordToAtlasCoordCommand
from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel
from slicereg.gui.commands import CommandProvider
from slicereg.io.tifffile import OmeTiffImageReader
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.models.section import Section
from slicereg.repos.atlas_repo import AtlasRepo


@scenario("features/section_affine_registration.feature", "Check Pixel Coordinate in Atlas Space")
def test_impl():
    ...


@pytest.fixture
def model():
    ome_reader = Mock(OmeTiffImageReader)
    ome_reader.read.return_value = Image(channels=np.empty((2, 3, 4)), resolution_um=12.)
    atlas_repo = AtlasRepo()
    atlas_repo.set_atlas(Atlas(volume=np.empty((2, 3, 4)), resolution_um=10))
    model = AppModel(_commands=CommandProvider(_atlas_repo=atlas_repo, _section_ome_reader=ome_reader))
    return model


@given("I have loaded a section")
def step_impl(model: AppModel):
    model.load_section("myfile.ome.tiff")


@when("I indicate a section image coordinate")
def step_impl(model: AppModel):
    model.select_coord(i=1, j=2)


@then("the coordinate's 2D position and 3D position should appear")
def step_impl(model: AppModel):
    assert model.selected_ij == (1, 2)
    assert isinstance(model.selected_xyz, tuple) and all(isinstance(el, float) for el in model.selected_xyz)
