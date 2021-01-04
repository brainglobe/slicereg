from abc import ABC, abstractmethod

from src.domain.atlas import Atlas
from src.domain.section import Section


class BaseUseCase(ABC):

    @abstractmethod
    def __call__(self, *args, **kwargs) -> None: ...


class BaseSectionRepo(ABC):

    @abstractmethod
    def get_section(self) -> Section: ...

    @abstractmethod
    def save_section(self, section: Section) -> None: ...


class BaseAtlasRepo(ABC):

    @abstractmethod
    def get_atlas(self, resolution_um: int) -> Atlas: ...

    @abstractmethod
    def get_current_atlas(self) -> Atlas: ...
