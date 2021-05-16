from unittest.mock import Mock

import numpy as np
import pytest

from slicereg.commands.base import BaseRepo
from slicereg.commands.register_section import RegisterSectionCommand
from slicereg.core import Atlas, Image, Section


@pytest.fixture
def repo():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = [Section(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4))]
    return repo


def test_register_section_command_gets_atlas_slice_image_when_both_section_and_atlas_are_loaded(repo):
    register_section = RegisterSectionCommand(_repo=repo)
    assert register_section().ok().atlas_slice_image.ndim == 2


def test_register_section_command_gets_sectin_transform_matrix_when_both_section_and_atlas_are_loaded(repo):
    register_section = RegisterSectionCommand(_repo=repo)
    assert register_section().ok().section_transform.shape == (4, 4)


def test_register_section_returns_error_message_if_no_section_loaded():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = []
    register_section = RegisterSectionCommand(_repo=repo)
    assert "no section" in register_section().value.lower()


def test_register_section_returns_error_message_if_no_atlas_loaded():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = None
    repo.get_sections.return_value = [Section(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4))]
    register_section = RegisterSectionCommand(_repo=repo)
    assert "no atlas" in register_section().value.lower()
