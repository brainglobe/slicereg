from typing import Optional

from src.models.section import Section
from src.workflows.load_section.load_section import BaseRepo


class SectionRepo(BaseRepo):

    def __init__(self):
        self._section: Optional[Section] = None

    def get_section(self) -> Optional[Section]:
        return self._section

    def set_section(self, section: Section) -> None:
        self._section = section
