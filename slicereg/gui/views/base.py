from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget


class BaseQtView(ABC):

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
