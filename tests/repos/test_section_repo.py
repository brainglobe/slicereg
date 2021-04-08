import pytest
import numpy as np

from slicereg.models.section import Section
from slicereg.models.image import Image
from slicereg.repos.section_repo import InMemorySectionRepo


@pytest.fixture
def repo():
    return InMemorySectionRepo()


@pytest.fixture
def section1():
    return Section(
        image=Image(channels=np.arange(12).reshape(2, 3, 2)),
        pixel_resolution_um=12,
    )


@pytest.fixture
def section2():
    return Section(
        image=Image(channels=np.arange(12).reshape(2, 3, 2)),
        pixel_resolution_um=12,
    )


def test_repo_stores_sections(repo, section1):
    assert not repo.sections
    assert len(repo.sections) == 0
    repo.save_section(section=section1)
    assert repo.sections
    assert len(repo.sections) == 1


def test_repo_stores_multiple_sections(repo, section1, section2):
    assert len(repo.sections) == 0
    repo.save_section(section=section1)
    assert len(repo.sections) == 1
    repo.save_section(section=section2)
    assert len(repo.sections) == 2


def test_repo_overwrites_existing_section(repo, section1: Section):
    assert len(repo.sections) == 0
    repo.save_section(section=section1)
    assert len(repo.sections) == 1
    repo.save_section(section=section1)
    assert len(repo.sections) == 1

    section_moved = section1.translate(x=3)
    repo.save_section(section=section_moved)
    assert len(repo.sections) == 1
