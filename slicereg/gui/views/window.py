from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel

from slicereg.commands.utils import Signal
from slicereg.gui.model import AppModel
from slicereg.gui.views.base import BaseQtWidget


class MainWindow(BaseQtWidget):

    def __init__(
            self,
            model: MainWindowViewModel,
            volume_widget: Optional[QWidget] = None,
            slice_widget: Optional[QWidget] = None,
            side_controls: Optional[QWidget] = None,
    ):
        self.model = model
        self.model.updated.connect(self.update)

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

    def update(self) -> None:
        self.win.setWindowTitle(self.model.title)

        if (ij := self.model.highlighted_image_coords) and (xyz := self.model.highlighted_physical_coords):
            self.image_coord_label.setText(f"(i={ij[0]}, j={ij[1]})   (x={xyz[0]:.1f}, y={xyz[1]:.1f}, z={xyz[2]:.1f})")


@dataclass
class MainWindowViewModel:
    _model: AppModel = field(repr=False)
    updated: Signal = field(default_factory=Signal, repr=False)

    @property
    def title(self) -> str:
        return self._model.window_title

    @property
    def highlighted_image_coords(self) -> Optional[Tuple[int, int]]:
        return self._model.highlighted_image_coords

    @property
    def highlighted_physical_coords(self) -> Optional[Tuple[float, float, float]]:
        return self._model.highlighted_physical_coords
