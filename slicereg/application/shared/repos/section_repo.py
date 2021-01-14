from __future__ import annotations

from typing import Optional, List, Tuple

from slicereg.models.section import Section
from slicereg.application.shared.repos.base import BaseSectionRepo


class InMemorySectionRepo(BaseSectionRepo):

    def __init__(self):
        self._sections: List[Section] = []

    @property
    def sections(self) -> List[Section]:
        return self._sections[:]

    def save_section(self, section: Section) -> None:
        if not self._sections:
            self._sections.append(section)
        else:
            self._sections[0] = section
