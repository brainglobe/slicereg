from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from src.gui.controller import Controller


class BaseVispyView(ABC):

    @abstractmethod
    def register_use_cases(self, app: Controller) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
