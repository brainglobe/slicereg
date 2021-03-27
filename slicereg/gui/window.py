from typing import Optional

from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QButtonGroup, \
    QHBoxLayout, QLabel, QSlider
from PySide2.QtCore import Qt
from vispy.app import Timer
import numpy as np

from slicereg.gui.base import BaseQtView
from slicereg.gui.slider import LabelledSliderWidget


class MainWindow(BaseQtView):

    def __init__(self, title: str = "", volume_widget: Optional[QWidget] = None, slice_widget: Optional[QWidget] = None):
        self.title = title
        self.volume_widget = volume_widget if volume_widget else QWidget()
        self.slice_widget = slice_widget if slice_widget else QWidget()

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

        side_layout = QVBoxLayout()
        main_layout.addLayout(side_layout)

        # Section Buttons
        load_image_button = QPushButton("Load Section")
        side_layout.addWidget(load_image_button)
        load_image_button.clicked.connect(self.show_load_image_dialog)

        # Scale Slider (Set Section Resolution)
        self.resample_widget = LabelledSliderWidget(min=1, max=100, default_text="Scale")
        side_layout.addLayout(self.resample_widget.layout)
        self.resample_widget.connect(self._on_resample_slider_released)


        # Atlas BUttons
        button_hbox = QHBoxLayout()
        side_layout.addLayout(button_hbox)

        atlas_buttons = QButtonGroup(self.win)
        atlas_buttons.setExclusive(True)
        atlas_buttons.buttonToggled.connect(self.atlas_button_toggled)

        

        for resolution in [100, 25, 10]:
            atlas_button = QPushButton(f"{resolution}um")
            atlas_button.setCheckable(True)
            button_hbox.addWidget(atlas_button)
            atlas_buttons.addButton(atlas_button)

            # The 10um atlas takes way too long to download at the moment.
            # It needs some kind of progress bar or async download feature to be useful.
            # The disabled button here shows it as an option for the future, but keeps it from being used.
            if resolution == 10:
                atlas_button.setDisabled(True)

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

    def on_image_coordinate_highlighted(self, image_coords, atlas_coords):
        i, j = image_coords
        x, y, z = atlas_coords
        self.image_coord_label.setText(f"(i={i}, j={j})      (x={x:.1f}, y={y:.1f}, z={z:.1f})")

    def on_error_raised(self, msg: str):
        self.show_temp_title(msg)

    def _on_resample_slider_released(self):
        resolution = self.resample_widget.value
        self.set_section_image_resolution(resolution_um=float(resolution))

    def set_section_image_resolution(self, resolution_um: float):
        raise NotImplementedError("Connect to ResampleSectionCommand before using.")
        
    def atlas_button_toggled(self, button: QPushButton, is_checked: bool):
        if not is_checked:  # Don't do anything for the button being unselected.
            return

        resolution_label = button.text()
        resolution = int("".join(filter(str.isdigit, resolution_label)))
        self.load_atlas(resolution=resolution)

    # Command Routing
    def show_load_image_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.win,
            caption="Load Image",
            dir="../data/RA_10X_scans/MEA",
            filter="OME-TIFF (*.ome.tiff)"
        )
        if not filename:
            return
        self.load_section(filename=filename)

    def load_atlas(self, resolution: int):
        raise NotImplementedError("Connect to LoadAtlasCommand before using.")

    def load_section(self, filename: str):
        raise NotImplementedError("Connect to a LoadImageCommand before using.")

    # View Code
    def _show_default_window_title(self):
        self.win.setWindowTitle(self._default_window_title)

    def show_temp_title(self, title: str) -> None:
        self.win.setWindowTitle(title)
        self.title_reset_timer.stop()
        self.title_reset_timer.start(iterations=1)
