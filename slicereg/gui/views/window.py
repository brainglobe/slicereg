from __future__ import annotations

from dataclasses import field, dataclass
from typing import Optional, Tuple

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel
from slicereg.gui.views.base import BaseQtWidget, BaseView


class MainWindow(BaseQtWidget, BaseView):

    def __init__(
            self,
            volume_widget: Optional[QWidget] = None,
            slice_widget: Optional[QWidget] = None,
            side_controls: Optional[QWidget] = None,
    ):
        BaseView.__init__(self)
        self.model: Optional[MainWindowViewModel] = None

        self.win = QMainWindow()

        widget = QWidget()
        self.win.setCentralWidget(widget)

        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        if slice_widget:
            main_layout.addWidget(slice_widget)

        if volume_widget:
            main_layout.addWidget(volume_widget)

        if side_controls:
            main_layout.addWidget(side_controls)

        self.statusbar = self.win.statusBar()
        self.image_coord_label = QLabel(text="Image Coords")
        self.statusbar.addPermanentWidget(self.image_coord_label)

        self.win.show()
        self.update()

    @property
    def qt_widget(self) -> QWidget:
        return self.win

    def update(self, **kwargs) -> None:
        if self.model is not None:
            self.win.setWindowTitle(self.model.title)

            if (ij := self.model.highlighted_image_coords) and (xyz := self.model.highlighted_physical_coords):
                self.image_coord_label.setText(f"(i={ij[0]}, j={ij[1]})   (x={xyz[0]:.1f}, y={xyz[1]:.1f}, z={xyz[2]:.1f})")


@dataclass(unsafe_hash=True)
class MainWindowViewModel:
    _model: AppModel = field(hash=False)
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        print(self.__class__.__name__, f"updated {kwargs}")
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
