from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget


class BaseQtWidget(ABC):

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...


class BaseView(ABC):

    @abstractmethod
    def update(self, **kwargs) -> None:
        ...

    def on_registration(self, model):
        """Overwriteable method that's called after the viewmodel is registered."""
        pass

    def register(self, model) -> None:
        model.updated.connect(self.update)
        self.on_registration(model=model)
