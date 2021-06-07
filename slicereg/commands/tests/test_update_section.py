from unittest.mock import Mock

import numpy as np
import pytest
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from slicereg.commands.base import BaseRepo
from slicereg.commands.constants import Axis, Direction, Plane
from slicereg.commands.update_section import UpdateSectionCommand, Center, Resample, \
    Translate, Rotate, SetPosition, SetRotation, Reorient, UpdateSectionRequest
from slicereg.core import Atlas, Image, Section
from slicereg.core.physical_transform import PhysicalTransformer


@pytest.fixture
def section1():
    return Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=PhysicalTransformer(x=5, y=10, z=2, rx=2, ry=15, rz=-3)
        )

@pytest.fixture
def section2():
    return Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=PhysicalTransformer(x=5, y=10, z=2, rx=2, ry=15, rz=-3)
        )


@pytest.fixture
def repo(section1, section2):
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = [section1, section2]
    repo.get_section.return_value = section1
    return repo


cases = [
    (Plane.Axial, 0, 90, 0),
    (Plane.Coronal, 90, 0, -90),
    (Plane.Sagittal, 0, 0, 0),
]
@pytest.mark.parametrize("plane,si,ap,lr", cases)
def test_reorient_section_sets_new_rotations(repo, section1, plane, si, ap, lr):
    command = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section1.id, steps=[Reorient(plane=plane)])
    result = command(request)
    data = result.ok()
    assert data.rot_longitudinal == si
    assert data.rot_anteroposterior == ap
    assert data.rot_horizontal == lr


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_position_translates_it_and_returns_new_position(value, axis):
    repo = Mock(BaseRepo)
    section = Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
                            physical_transform=PhysicalTransformer(x=5, y=10, z=2))
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_section.return_value = section
    move_section = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section.id, steps=[SetPosition(axis=axis, value=value)])
    result = move_section(request)
    data = result.unwrap()
    assert data.superior == value if axis is Axis.Longitudinal else 5
    assert data.anterior == value if axis is Axis.Anteroposterior else 10
    assert data.right == value if axis is Axis.Horizontal else 2


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_rotation_rotates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(rx=5, ry=10, rz=2)
    section = Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
                            physical_transform=physical_transform)
    repo = Mock(BaseRepo)
    repo.get_section.return_value = section

    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section.id, steps=[SetRotation(axis=axis, value=value)])
    result = move_section(request)
    data = result.unwrap()
    assert data.rot_longitudinal == value if axis is Axis.Longitudinal else 5
    assert data.rot_anteroposterior == value if axis is Axis.Anteroposterior else 10
    assert data.rot_horizontal == value if axis is Axis.Horizontal else 2


@given(value=floats(-100, 100), direction=sampled_from(Direction))
def test_relative_move_section_to_position_translates_it_and_returns_new_position(value, direction):
    physical_transform = PhysicalTransformer(x=5, y=10, z=2)
    section = Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
                            physical_transform=physical_transform)
    repo = Mock(BaseRepo)
    repo.get_section.return_value = section
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section.id, steps=[Translate(direction=direction, value=value)])
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
    section = Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4), physical_transform=physical_transform)
    repo = Mock(BaseRepo)
    repo.get_section.return_value = section
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section.id, steps=[Rotate(axis=axis, value=value)])
    result = move_section(request)
    data = result.unwrap()

    assert data.rot_longitudinal == value + 5 if axis is Axis.Longitudinal else 5
    assert data.rot_anteroposterior == value + 10 if axis is Axis.Anteroposterior else 10
    assert data.rot_horizontal == value + 2 if axis is Axis.Horizontal else 2


def test_update_section_updates_multiple_times_if_given_multiple_commands(repo, section1):
    command = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section1.id, steps=[Translate(Direction.Right, 30), Translate(Direction.Right, 400)])
    result = command(request)
    data = result.ok()
    assert data.right == 2 + 30 + 400


def test_center_atlas_command_centers_section_when_atlas_is_loaded():
    section = Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
                            physical_transform=PhysicalTransformer(x=0, y=0, z=0), )
    repo = Mock(BaseRepo)
    repo.get_section.return_value = section
    repo.get_atlas.return_value = Atlas(volume=np.empty((3, 3, 3)), annotation_volume=np.empty((3, 3, 3)),
                                        resolution_um=10)
    move_section = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section.id, steps=[Center()])
    result = move_section(request)
    data = result.unwrap()
    assert data.superior == 15
    assert data.anterior == 15
    assert data.right == 15


def test_resample_section_gets_section_with_requested_resolution_and_different_image_size(repo, section1):
    resample_section = UpdateSectionCommand(_repo=repo)
    request = UpdateSectionRequest(section_id=section1.id, steps=[Resample(resolution_um=5)])
    result = resample_section(request)
    assert result.unwrap().resolution_um == 5
    assert result.unwrap().section_image.shape == (3, 3)


def test_register_section_command_gets_atlas_slice_image_when_both_section_and_atlas_are_loaded(repo, section1):
    command = UpdateSectionCommand(_repo=repo)
    result = command(UpdateSectionRequest(section_id=section1.id, steps=[]))
    assert result.ok().atlas_slice_image.ndim == 2


def test_register_section_gets_section_transform_matrix_when_both_section_and_atlas_are_loaded(repo, section1):
    command = UpdateSectionCommand(_repo=repo)
    result = command(UpdateSectionRequest(section_id=section1.id, steps=[]))
    assert result.ok().section_transform.shape == (4, 4)


def test_register_section_returns_error_message_if_no_section_loaded(section1):
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_section.return_value = None
    command = UpdateSectionCommand(_repo=repo)
    result = command(UpdateSectionRequest(section_id=section1.id, steps=[]))
    assert "section not found" in result.value.lower()


def test_register_section_returns_error_message_if_no_atlas_loaded(section1):
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = None
    repo.get_sections.return_value = [Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4))]
    command = UpdateSectionCommand(_repo=repo)
    result = command(UpdateSectionRequest(section_id=section1.id, steps=[]))
    assert "no atlas" in result.value.lower()


def test_register_section_returns_2d_orthogonal_atlas_section_images_at_section_position(repo, section1):
    command = UpdateSectionCommand(_repo=repo)
    result = command(UpdateSectionRequest(section_id=section1.id, steps=[]))
    data = result.ok()
    assert data.coronal_atlas_image.ndim == 2
    assert data.axial_atlas_image.ndim == 2
    assert data.sagittal_atlas_image.ndim == 2


def test_update_section_command_works_on_section_with_matching_id(repo, section1: Section, section2):
    command = UpdateSectionCommand(_repo=repo)
    result = command(UpdateSectionRequest(section_id=section1.id, steps=[Center()]))
    assert result.is_ok()
    data = result.ok()
    assert data.section_id == section1.id
    repo.get_section.assert_called_with(id=section1.id)
