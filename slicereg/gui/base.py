from abc import abstractmethod, ABC

from PySide2.QtWidgets import QWidget

from slicereg.commands.provider import CommandProvider


class BaseVispyView(ABC):

    @abstractmethod
    def register_commands(self, app: CommandProvider) -> None: ...

    @property
    @abstractmethod
    def qt_widget(self) -> QWidget: ...
