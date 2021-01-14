from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from slicereg.application.provider import WorkflowProvider


class BaseVispyView(ABC):

    @abstractmethod
    def register_workflows(self, app: WorkflowProvider) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
