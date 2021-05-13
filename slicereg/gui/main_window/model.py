from dataclasses import dataclass, field
from typing import Optional, Tuple

from slicereg.utils.signal import Signal
from slicereg.app.app_model import AppModel


@dataclass(unsafe_hash=True)
class MainWindowViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)
    footer: str = ""

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if hasattr(self, 'updated'):
            self.updated.emit(changed=key)

    def update(self, changed: str):
        if changed in ['selected_ij', 'selected_xyz']:
            self._update_footer()

    @property
    def title(self) -> str:
        return self._model.window_title

    def _update_footer(self):
        ij = self._model.selected_ij
        xyz = self._model.selected_xyz
        text = f"(i={ij[0]}, j={ij[1]})   (x={xyz[0]:.1f}, y={xyz[1]:.1f}, z={xyz[2]:.1f})"
        self.footer = text

    @property
    def highlighted_image_coords(self) -> Optional[Tuple[int, int]]:
        return self._model.selected_ij

    @property
    def highlighted_physical_coords(self) -> Optional[Tuple[float, float, float]]:
        return self._model.selected_xyz
