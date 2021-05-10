from __future__ import annotations

from typing import List, Dict
from uuid import UUID

from slicereg.commands.base import BaseSectionRepo
from slicereg.models.section import Section


class SectionRepo(BaseSectionRepo):

    def __init__(self):
        self._sections: Dict[UUID, Section] = {}

    @property
    def sections(self) -> List[Section]:
        return list(self._sections.values())

    def save_section(self, section: Section) -> None:
        self._sections[section.id] = section

