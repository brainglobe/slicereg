from dataclasses import dataclass, field
from typing import Optional, Tuple

from slicereg.utils.signal import Signal
from slicereg.app.app_model import AppModel


@dataclass(unsafe_hash=True)
class MainWindowViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        self.updated.emit(**kwargs)

    @property
    def title(self) -> str:
        return self._model.window_title

    @property
    def highlighted_image_coords(self) -> Optional[Tuple[int, int]]:
        return self._model.selected_ij

    @property
    def highlighted_physical_coords(self) -> Optional[Tuple[float, float, float]]:
        return self._model.selected_xyz
