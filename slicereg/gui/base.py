from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget


class BaseQtWidget(ABC):

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
