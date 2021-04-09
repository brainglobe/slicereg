from unittest.mock import Mock

import numpy as np
import pytest
from pytest_bdd import scenario, given, when, then
from numpy import random

from slicereg.commands.base import BaseSectionRepo
from slicereg.repos.atlas_repo import BaseAtlasRepo
from slicereg.commands.update_section_transform import UpdateSectionTransformCommand
from slicereg.commands.utils import Signal
from slicereg.models.atlas import Atlas
from slicereg.models.image import Image
from slicereg.models.section import Section
from slicereg.models.transforms import Transform3D

@scenario("section_affine_registration.feature", "Set Section's 3D Coordinates")
def test_impl():
    ...


@pytest.fixture
def repo():
    repo = Mock(BaseSectionRepo)
    repo.sections = [
        Section(
            image=Image(channels=np.random.random((2, 3, 4))),
            pixel_resolution_um=12.,
            plane_3d=Transform3D(x=5, y=2, z=20),
        )
    ]
    return repo

@pytest.fixture
def atlas_repo():
    repo = Mock(BaseAtlasRepo)
    repo.get_atlas.return_value = Atlas(
        volume=random.normal(size=(10, 10, 10)),
        resolution_um=25,
    )
    return repo

@pytest.fixture
def command(repo, atlas_repo):
    return UpdateSectionTransformCommand(_section_repo=repo, _atlas_repo=atlas_repo, section_moved=Mock(Signal))


@given("I have loaded a section")
def step_impl(repo: BaseSectionRepo):
    assert len(repo.sections) == 1


@when("I give new translation and/or rotation values")
def step_impl(command: UpdateSectionTransformCommand):
    command(x=2, y=5, z=10, rx=0, ry=0, rz=0)


@then("the image is updated with a new 3D transform with indicated paramters set to the requested value")
def step_impl(command: UpdateSectionTransformCommand):
    output = command.section_moved.emit.call_args[1]
    assert 'transform' in output
    transform = output['transform']
    assert transform.shape == (4, 4)


@then("an atlas section image at that transform is shown.")
def step_impl(command: UpdateSectionTransformCommand):
    output = command.section_moved.emit.call_args[1]
    assert isinstance(output.get('atlas_slice_image'), np.ndarray) and output['atlas_slice_image'].ndim == 2
