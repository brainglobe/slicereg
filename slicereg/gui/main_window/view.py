from __future__ import annotations

from typing import Optional

from PySide2 import QtCore
from PySide2.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout

from slicereg.gui.base import BaseQtWidget
from slicereg.gui.main_window.model import MainWindowViewModel


class MainWindowView(BaseQtWidget):

    def __init__(
            self,
            _model: MainWindowViewModel,
            coronal_widget: Optional[QWidget] = None,
            axial_widget: Optional[QWidget] = None,
            sagittal_widget: Optional[QWidget] = None,
            volume_widget: Optional[QWidget] = None,
            slice_widget: Optional[QWidget] = None,
            side_controls: Optional[QWidget] = None,
    ):

        self._model = _model
        self._model.updated.connect(self.update)

        self.win = QMainWindow()

        widget = QWidget()
        self.win.setCentralWidget(widget)

        main_layout = QHBoxLayout()
        top_views_layout = QHBoxLayout()
        bottom_views_layout = QHBoxLayout()
        views_layout = QVBoxLayout()
        views_layout.addLayout(top_views_layout)
        views_layout.addLayout(bottom_views_layout)
        main_layout.addLayout(views_layout)
        widget.setLayout(main_layout)

        if coronal_widget:
            coronal_layout = QVBoxLayout()
            label = QLabel('Coronal')
            label.setAlignment(QtCore.Qt.AlignCenter)
            coronal_layout.addWidget(label)
            coronal_layout.addWidget(coronal_widget)
            top_views_layout.addLayout(coronal_layout)

        if axial_widget:
            axial_layout = QVBoxLayout()
            label = QLabel('Axial')
            label.setAlignment(QtCore.Qt.AlignCenter)
            axial_layout.addWidget(label)
            axial_layout.addWidget(axial_widget)
            top_views_layout.addLayout(axial_layout)

        if sagittal_widget:
            sagittal_layout = QVBoxLayout()
            label = QLabel('Sagittal')
            label.setAlignment(QtCore.Qt.AlignCenter)
            sagittal_layout.addWidget(label)
            sagittal_layout.addWidget(sagittal_widget)
            top_views_layout.addLayout(sagittal_layout)

        if slice_widget:
            bottom_views_layout.addWidget(slice_widget)

        if volume_widget:
            bottom_views_layout.addWidget(volume_widget)

        if side_controls:
            main_layout.addWidget(side_controls)

        self.statusbar = self.win.statusBar()
        self.image_coord_label = QLabel(text="Image Coords")
        self.statusbar.addPermanentWidget(self.image_coord_label)

        self.win.show()

    @property
    def qt_widget(self) -> QWidget:
        return self.win

    def update(self, changed: str) -> None:
        render_funs = {
            'title': self._render_title,
            'footer': self._render_footer,
        }
        render_funs[changed]()

    def _render_title(self):
        self.win.setWindowTitle(self._model.title)

    def _render_footer(self):
        self.image_coord_label.setText(self._model.footer)
