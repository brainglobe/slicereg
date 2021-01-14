from __future__ import annotations

from typing import Optional, List, Tuple

from slicereg.models.section import Section
from slicereg.application.shared.repos.base import BaseSectionRepo


class InMemorySectionRepo(BaseSectionRepo):

    def __init__(self):
        self.__sections: List[Section] = []

    @property
    def sections(self) -> List[Section]:
        return self.__sections[:]

    def save_section(self, section: Section) -> None:
        self.__sections.append(section)
