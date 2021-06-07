from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from slicereg.core.atlas import Atlas
from slicereg.core.section import Section


class BaseRepo(ABC):

    @abstractmethod
    def get_section(self, id: UUID) -> Optional[Section]: ...

    @abstractmethod
    def get_sections(self) -> List[Section]: ...

    @abstractmethod
    def save_section(self, section: Section): ...

    @abstractmethod
    def get_atlas(self) -> Optional[Atlas]: ...

    @abstractmethod
    def set_atlas(self, atlas: Atlas) -> None: ...
