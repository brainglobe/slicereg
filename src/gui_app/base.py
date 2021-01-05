from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from src.gui_app.use_cases import UseCaseProvider


class BaseVispyView(ABC):

    @abstractmethod
    def register_use_cases(self, app: UseCaseProvider) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
