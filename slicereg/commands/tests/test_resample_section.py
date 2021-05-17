from unittest.mock import Mock

import numpy as np

from slicereg.commands.base import BaseRepo
from slicereg.commands.resample_section import ResampleSectionCommand
from slicereg.core import Section, Image


def test_resample_section_gets_section_with_requested_resolution_and_different_image_size():
    repo = Mock(BaseRepo)
    repo.get_sections.return_value = repo.get_sections.return_value = [
        Section.create(image=Image(channels=np.empty((2, 4, 4)), resolution_um=10))
    ]
    resample_section = ResampleSectionCommand(_repo=repo)
    result = resample_section(resolution_um=5)
    assert result.unwrap().resolution_um == 5
    assert result.unwrap().section_image.shape == (8, 8)
