from unittest.mock import Mock

import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from slicereg.commands.base import BaseRepo
from slicereg.commands.constants import Axis, Direction
from slicereg.commands.update_section import UpdateSectionCommand, CenterRequest, ResampleRequest, \
    TranslateRequest, RotateRequest, SetPositionRequest, SetRotationRequest
from slicereg.core import Atlas, Image, Section
from slicereg.core.physical_transform import PhysicalTransformer


@pytest.fixture
def repo():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=PhysicalTransformer(x=5, y=10, z=2)
        )
    ]
    return repo


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_position_translates_it_and_returns_new_position(value, axis):
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=PhysicalTransformer(x=5, y=10, z=2)
        )
    ]
    move_section = UpdateSectionCommand(_repo=repo)
    request = SetPositionRequest(axis=axis, value=value)
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
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = SetRotationRequest(axis=axis, value=value)
    result = move_section(request=request)
    data = result.unwrap()
    assert data.rot_longitudinal == value if axis is Axis.Longitudinal else 5
    assert data.rot_anteroposterior == value if axis is Axis.Anteroposterior else 10
    assert data.rot_horizontal == value if axis is Axis.Horizontal else 2


@given(value=floats(-100, 100), direction=sampled_from(Direction))
def test_relative_move_section_to_position_translates_it_and_returns_new_position(value, direction):
    physical_transform = PhysicalTransformer(x=5, y=10, z=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = TranslateRequest(direction=direction, value=value)
    result = move_section(request)
    data = result.unwrap()
    if direction is Direction.Superior:
        assert data.superior == 5 + value
    elif direction is Direction.Inferior:
        assert data.superior == 5 - value
    else:
        assert data.superior == 5

    if direction is Direction.Anterior:
        assert data.anterior == 10 + value
    elif direction is Direction.Posterior:
        assert data.anterior == 10 - value
    else:
        assert data.anterior == 10

    if direction is Direction.Right:
        assert data.right == 2 + value
    elif direction is Direction.Left:
        assert data.right == 2 - value
    else:
        assert data.right == 2


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
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = RotateRequest(axis=axis, value=value)
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
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
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
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    resample_section = UpdateSectionCommand(_repo=repo)
    request = ResampleRequest(resolution_um=5)
    result = resample_section(request)
    assert result.unwrap().resolution_um == 5
    assert result.unwrap().section_image.shape == (8, 8)


def test_register_section_command_gets_atlas_slice_image_when_both_section_and_atlas_are_loaded(repo):
    command = UpdateSectionCommand(_repo=repo)
    result = command(CenterRequest())
    assert result.ok().atlas_slice_image.ndim == 2


def test_register_section_gets_section_transform_matrix_when_both_section_and_atlas_are_loaded(repo):
    command = UpdateSectionCommand(_repo=repo)
    result = command(CenterRequest())
    assert result.ok().section_transform.shape == (4, 4)


def test_register_section_returns_error_message_if_no_section_loaded():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = []
    command = UpdateSectionCommand(_repo=repo)
    result = command(CenterRequest())
    assert "no section" in result.value.lower()


def test_register_section_returns_error_message_if_no_atlas_loaded():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = None
    repo.get_sections.return_value = [Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4))]
    command = UpdateSectionCommand(_repo=repo)
    result = command(CenterRequest())
    assert "no atlas" in result.value.lower()


def test_register_section_returns_2d_orthogonal_atlas_section_images_at_section_position(repo):
    command = UpdateSectionCommand(_repo=repo)
    result = command(CenterRequest())
    data = result.ok()
    assert data.coronal_atlas_image.ndim == 2
    assert data.axial_atlas_image.ndim == 2
    assert data.sagittal_atlas_image.ndim == 2
