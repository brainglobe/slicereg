from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget


class BaseQtWidget(ABC):

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...


class BaseViewModel(ABC):
    ...


class BaseView(ABC):

    @abstractmethod
    def update(self, model: BaseViewModel) -> None:  ...

    @abstractmethod
    def register_viewmodel(self, model: BaseViewModel) -> None: ...