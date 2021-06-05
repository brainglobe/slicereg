from unittest.mock import Mock

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from slicereg.commands.base import BaseRepo
from slicereg.commands.move_section2 import MoveType, MoveSectionCommand2, MoveRequest, CenterRequest, ResampleRequest
from slicereg.commands.constants import Axis
from slicereg.core import Section, Image, Atlas
from slicereg.core.physical_transform import PhysicalTransformer


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_position_translates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(x=5, y=10, z=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    move_section = MoveSectionCommand2(_repo=repo)
    request = MoveRequest(axis=axis, value=value, move_type=MoveType.TRANSLATION, absolute=True)
    result = move_section(request=request)
    data = result.unwrap()
    assert data.superior == value if axis is Axis.Longitudinal else 5
    assert data.anterior == value if axis is Axis.Anteroposterior else 10
    assert data.right == value if axis is Axis.Horizontal else 2


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_rotation_rotates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(rx=5, ry=10, rz=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    move_section = MoveSectionCommand2(_repo=repo)
    request = MoveRequest(axis=axis, value=value, move_type=MoveType.ROTATION, absolute=True)
    result = move_section(request=request)
    data = result.unwrap()
    assert data.rot_longitudinal == value if axis is Axis.Longitudinal else 5
    assert data.rot_anteroposterior == value if axis is Axis.Anteroposterior else 10
    assert data.rot_horizontal == value if axis is Axis.Horizontal else 2



@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_relative_move_section_to_position_translates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(x=5, y=10, z=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    move_section = MoveSectionCommand2(_repo=repo)
    request = MoveRequest(axis=axis, value=value, move_type=MoveType.TRANSLATION, absolute=False)
    result = move_section(request)
    data = result.unwrap()
    assert data.superior == value + 5 if axis is Axis.Longitudinal else 5
    assert data.anterior == value + 10 if axis is Axis.Anteroposterior else 10
    assert data.right == value + 2 if axis is Axis.Horizontal else 2


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_relative_move_section_to_rotation_rotates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(rx=5, ry=10, rz=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    move_section = MoveSectionCommand2(_repo=repo)
    request = MoveRequest(axis=axis, value=value, move_type=MoveType.ROTATION, absolute=False)
    result = move_section(request=request)
    data = result.unwrap()
    assert data.rot_longitudinal == value + 5 if axis is Axis.Longitudinal else 5
    assert data.rot_anteroposterior == value + 10 if axis is Axis.Anteroposterior else 10
    assert data.rot_horizontal == value + 2 if axis is Axis.Horizontal else 2


def test_center_atlas_command_translates_section_when_atlas_is_loaded():
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=PhysicalTransformer(x=0, y=0, z=0),
        )
    ]
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)), resolution_um=10)
    move_section = MoveSectionCommand2(_repo=repo)
    request = CenterRequest()
    result = move_section(request)
    data = result.unwrap()
    assert data.superior == 15
    assert data.anterior == 15
    assert data.right == 15


def test_resample_section_gets_section_with_requested_resolution_and_different_image_size():
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = repo.get_sections.return_value = [
        Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=10))
    ]
    resample_section = MoveSectionCommand2(_repo=repo)
    request = ResampleRequest(resolution_um=5)
    result = resample_section(request)
    assert result.unwrap().resolution_um == 5
    assert result.unwrap().section_image.shape == (8, 8)
