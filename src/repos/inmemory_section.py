from typing import Optional

from src.core.section.base import BaseSectionRepo
from src.core.section.models import Section


class InMemorySectionRepo(BaseSectionRepo):

    def __init__(self):
        self.section: Optional[Section] = None

    def get_section(self) -> Optional[Section]:
        return self.section

    def save_section(self, section: Section) -> None:
        self.section = section


