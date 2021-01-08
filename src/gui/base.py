from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from src.gui.viewmodel import ViewModel


class BaseVispyView(ABC):

    @abstractmethod
    def register_use_cases(self, app: ViewModel) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
