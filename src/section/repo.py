from typing import Optional

from src.section.base import BaseSectionRepo
from src.section.models import Section


class InMemorySectionRepo(BaseSectionRepo):

    def __init__(self):
        self.section: Optional[Section] = None

    def get_section(self) -> Optional[Section]:
        return self.section

    def save_section(self, section: Section) -> None:
        self.section = section


