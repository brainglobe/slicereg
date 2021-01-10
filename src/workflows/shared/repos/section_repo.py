from __future__ import annotations

from typing import Optional

from src.models.section import Section
from src.workflows.shared.repos.base import BaseSectionRepo


class InMemorySectionRepo(BaseSectionRepo):
    __section: Optional[Section] = None

    def get_section(self) -> Optional[Section]:
        return self.__class__.__section

    def set_section(self, section: Section) -> None:
        self.__class__.__section = section
