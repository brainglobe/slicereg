from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from src.gui.workflows import WorkflowProvider


class BaseVispyView(ABC):

    @abstractmethod
    def register_use_cases(self, app: WorkflowProvider) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
