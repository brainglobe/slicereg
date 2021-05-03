from abc import abstractmethod, ABC
from typing import Optional

from PySide2.QtWidgets import QWidget

from slicereg.commands.utils import Signal
from slicereg.gui.commands import CommandProvider
from slicereg.gui.app_model import AppModel


class BaseQtWidget(ABC):

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...


class BaseView(ABC):

    @abstractmethod
    def update(self, **kwargs) -> None:
        ...

    def on_registration(self, model=None):
        """Overwriteable method that's called after the viewmodel is registered."""
        pass

    def register(self, model) -> None:
        model.updated.connect(self.update)
        self.on_registration(model=model)
