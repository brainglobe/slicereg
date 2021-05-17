import numpy as np

from slicereg.core.atlas import Atlas
from slicereg.core.image import Image
from slicereg.core.section import Section
from slicereg.repos import InMemoryRepo


def test_repo_starts_with_no_atlas():
    repo = InMemoryRepo()
    assert repo.get_atlas() is None


def test_repo_can_round_trip_atlas():
    repo = InMemoryRepo()
    atlas = Atlas(volume=np.random.random((3, 3, 3)), resolution_um=1)
    repo.set_atlas(atlas=atlas)
    assert repo.get_atlas() == atlas


def test_repo_stores_multiple_sections():
    repo = InMemoryRepo()
    section1 = Section.create(image=Image(channels=np.empty((2, 3, 4)), resolution_um=12))
    section2 = Section.create(image=Image(channels=np.empty((2, 3, 4)), resolution_um=12))
    assert len(repo.get_sections()) == 0
    repo.save_section(section=section1)
    assert len(repo.get_sections()) == 1
    repo.save_section(section=section2)
    assert len(repo.get_sections()) == 2


def test_repo_overwrites_existing_section_even_if_properties_change():
    repo = InMemoryRepo()
    section = Section.create(image=Image(channels=np.empty((2, 3, 4)), resolution_um=12))
    repo.save_section(section=section)
    assert len(repo.get_sections()) == 1
    repo.save_section(section=section)
    assert len(repo.get_sections()) == 1

    section_moved = section.update(image=section.image.update(resolution_um=14))
    repo.save_section(section=section_moved)
    assert len(repo.get_sections()) == 1
