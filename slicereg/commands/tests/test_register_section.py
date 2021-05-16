from unittest.mock import Mock

import numpy as np

from slicereg.commands.base import BaseRepo
from slicereg.commands.register_section import RegisterSectionCommand
from slicereg.core import Atlas, Image, Section


def test_register_section_command_gets_atlas_slice_image_when_both_section_and_atlas_are_loaded():
    repo = Mock(BaseRepo)
    repo.get_atlas.return_value = Atlas(volume=np.empty((5, 5, 5)), resolution_um=10)
    repo.get_sections.return_value = [Section(image=Image(channels=np.empty((2, 4, 4)), resolution_um=3.4))]
    register_section = RegisterSectionCommand(_repo=repo)
    assert register_section().ok().atlas_slice_image.ndim == 2
