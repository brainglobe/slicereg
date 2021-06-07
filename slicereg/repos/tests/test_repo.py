from unittest.mock import Mock
from uuid import uuid4

from slicereg.core.atlas import Atlas
from slicereg.core.section import Section
from slicereg.repos import InMemoryRepo


def test_repo_starts_with_no_atlas():
    repo = InMemoryRepo()
    assert repo.get_atlas() is None


def test_repo_can_round_trip_atlas():
    repo = InMemoryRepo()
    atlas = Mock(Atlas)
    repo.set_atlas(atlas=atlas)
    assert repo.get_atlas() == atlas


def test_repo_stores_multiple_sections():
    repo = InMemoryRepo()
    section1 = Mock(Section, id='a')
    section2 = Mock(Section, id='b')
    assert len(repo.get_sections()) == 0
    repo.save_section(section=section1)
    assert len(repo.get_sections()) == 1
    repo.save_section(section=section2)
    assert len(repo.get_sections()) == 2


def test_repo_overwrites_existing_section_even_if_properties_change():
    repo = InMemoryRepo()
    section = Mock(Section, id=3)
    repo.save_section(section=section)
    assert len(repo.get_sections()) == 1
    repo.save_section(section=section)
    assert len(repo.get_sections()) == 1

    section_moved = Mock(Section, id=section.id)
    repo.save_section(section=section_moved)
    assert len(repo.get_sections()) == 1


def test_repo_gets_section_with_matching_id():
    repo = InMemoryRepo()
    section1 = Mock(Section, id=uuid4())
    section2 = Mock(Section, id=uuid4())
    repo.save_section(section1)
    repo.save_section(section2)

    assert repo.get_section(id=section2.id) is section2
    assert repo.get_section(id=section1.id) is section1
    assert repo.get_section(id=section2.id) is section2


def test_repo_gets_none_when_no_matching_section_found():
    repo = InMemoryRepo()
    section1 = Mock(Section, id=uuid4())
    section2 = Mock(Section, id=uuid4())
    repo.save_section(section1)
    repo.save_section(section2)

    assert repo.get_section(id=uuid4()) is None
