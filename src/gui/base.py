from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from src.workflows.provider import Provider


class BaseVispyView(ABC):

    @abstractmethod
    def register_use_cases(self, app: Provider) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
