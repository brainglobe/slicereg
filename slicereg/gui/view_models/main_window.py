from dataclasses import dataclass, field
from typing import Optional, Tuple

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel


@dataclass(unsafe_hash=True)
class MainWindowViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs.keys()}")
        self.updated.emit(**kwargs)

    @property
    def title(self) -> str:
        return self._model.window_title

    @property
    def highlighted_image_coords(self) -> Optional[Tuple[int, int]]:
        return self._model.highlighted_image_coords

    @property
    def highlighted_physical_coords(self) -> Optional[Tuple[float, float, float]]:
        return self._model.highlighted_physical_coords
