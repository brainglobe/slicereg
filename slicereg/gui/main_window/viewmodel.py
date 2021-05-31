from dataclasses import dataclass, field
from typing import Optional, Tuple

from slicereg.gui.app_model import AppModel
from slicereg.utils.observable import HasObservableAttributes


@dataclass(unsafe_hash=True)
class MainWindowViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    footer: str = ""

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        if changed in ['selected_ij', 'selected_xyz']:
            self._update_footer()

    @property
    def title(self) -> str:
        return self._model.window_title

    def _update_footer(self):
        xyz = self._model.selected_xyz
        text = f"(x={xyz[0]:.1f}, y={xyz[1]:.1f}, z={xyz[2]:.1f})"
        self.footer = text

    @property
    def highlighted_physical_coords(self) -> Optional[Tuple[float, float, float]]:
        return self._model.selected_xyz
