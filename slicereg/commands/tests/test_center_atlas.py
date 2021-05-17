from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.commands.base import BaseRepo
from slicereg.commands.center_section import CenterSectionCommand
from slicereg.core import Atlas, Image, Section
from slicereg.core.physical_transform import PhysicalTransformer


@pytest.fixture
def repo():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = [
        Section.create(
            image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4),
            physical_transform=PhysicalTransformer(x=0, y=0, z=0)
        )
    ]
    return repo


def test_center_atlas_command_translates_section_when_atlas_is_loaded(repo):
    center_section = CenterSectionCommand(_repo=repo)
    result = center_section()
    data = result.unwrap()
    assert data.x != 0
    assert data.y != 0
    assert data.z != 0

