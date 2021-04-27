from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel
from vispy.app import Timer

from slicereg.commands.utils import Signal
from slicereg.gui.model import AppModel
from slicereg.gui.views.base import BaseQtView


class MainWindow(BaseQtView):

    def __init__(
            self,
            model: MainWindowViewModel,
            title: str = "",
            volume_widget: Optional[QWidget] = None,
            slice_widget: Optional[QWidget] = None,
            side_controls: Optional[QWidget] = None,
    ):
        self.model = model
        self.model.updated.connect(self.update)

        self.title = title
        self.volume_widget = volume_widget if volume_widget else QWidget()
        self.slice_widget = slice_widget if slice_widget else QWidget()
        self.side_widget = side_controls if side_controls else QWidget()

        self._init()

    def _init(self):
        print("Building...")

        self.win = QMainWindow()
        self._default_window_title = self.title

        widget = QWidget()
        self.win.setCentralWidget(widget)

        main_layout = QHBoxLayout()
        widget.setLayout(main_layout)

        main_layout.addWidget(self.slice_widget)
        main_layout.addWidget(self.volume_widget)
        main_layout.addWidget(self.side_widget)

        self.title_reset_timer = Timer(interval=2, connect=lambda e: self._show_default_window_title(), iterations=1,
                                       start=False)
        self._show_default_window_title()

        self.statusbar = self.win.statusBar()

        self.image_coord_label = QLabel(text="Image Coords")
        self.statusbar.addPermanentWidget(self.image_coord_label)

        self.win.show()

    @property
    def qt_widget(self) -> QWidget:
        return self.win

    def update(self) -> None:
        if (ij := self.model.highlighted_image_coords) and (xyz := self.model.highlighted_physical_coords):
            self.image_coord_label.setText(f"(i={ij[0]}, j={ij[1]})   (x={xyz[0]:.1f}, y={xyz[1]:.1f}, z={xyz[2]:.1f})")

    def on_error_raised(self, msg: str):
        self.show_temp_title(msg)

    # View Code
    def _show_default_window_title(self):
        self.win.setWindowTitle(self._default_window_title)

    def show_temp_title(self, title: str) -> None:
        self.win.setWindowTitle(title)
        self.title_reset_timer.stop()
        self.title_reset_timer.start(iterations=1)


@dataclass
class MainWindowViewModel:
    _model: AppModel = field(repr=False)
    updated: Signal = field(default_factory=Signal, repr=False)

    @property
    def highlighted_image_coords(self) -> Optional[Tuple[int, int]]:
        return self._model.highlighted_image_coords

    @property
    def highlighted_physical_coords(self) -> Optional[Tuple[float, float, float]]:
        return self._model.highlighted_physical_coords
