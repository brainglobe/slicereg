import numpy as np

from slicereg.models.image import Image
from slicereg.models.section import Section
from slicereg.repos.section_repo import InMemorySectionRepo


def test_repo_stores_multiple_sections():
    section1 = Section(image=Image(channels=np.empty((2, 3, 4)), resolution_um=12))
    section2 = Section(image=Image(channels=np.empty((2, 3, 4)), resolution_um=12))
    repo = InMemorySectionRepo()
    assert len(repo.sections) == 0
    repo.save_section(section=section1)
    assert len(repo.sections) == 1
    repo.save_section(section=section2)
    assert len(repo.sections) == 2


def test_repo_overwrites_existing_section_even_if_properties_change():
    section = Section(image=Image(channels=np.empty((2, 3, 4)), resolution_um=12))
    repo = InMemorySectionRepo()
    repo.save_section(section=section)
    assert len(repo.sections) == 1
    repo.save_section(section=section)
    assert len(repo.sections) == 1

    section_moved = section.update(image=section.image.update(resolution_um=14))
    repo.save_section(section=section_moved)
    assert len(repo.sections) == 1
