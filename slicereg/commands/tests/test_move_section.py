from unittest.mock import Mock

import numpy as np
from hypothesis import given
from hypothesis.strategies import floats, sampled_from

from slicereg.commands.base import BaseRepo
from slicereg.commands.move_section2 import MoveType, Axis, MoveSectionCommand2
from slicereg.core import Section, Image
from slicereg.core.physical_transform import PhysicalTransformer


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_position_translates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(x=5, y=10, z=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    move_section = MoveSectionCommand2(_repo=repo)
    result = move_section(axis=axis, value=value, type=MoveType.TRANSLATION, absolute=True)
    data = result.unwrap()
    assert data.x == value if axis is Axis.X else 5
    assert data.y == value if axis is Axis.Y else 10
    assert data.z == value if axis is Axis.Z else 2


@given(value=floats(-100, 100), axis=sampled_from(Axis))
def test_move_section_to_rotation_rotates_it_and_returns_new_position(value, axis):
    physical_transform = PhysicalTransformer(rx=5, ry=10, rz=2)
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = [
        Section(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=physical_transform
        )
    ]
    move_section = MoveSectionCommand2(_repo=repo)
    result = move_section(axis=axis, value=value, type=MoveType.ROTATION, absolute=True)
    data = result.unwrap()
    assert data.rx == value if axis is Axis.X else 5
    assert data.ry == value if axis is Axis.Y else 10
    assert data.rz == value if axis is Axis.Z else 2
