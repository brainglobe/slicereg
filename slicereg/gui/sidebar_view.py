from functools import partial

from PySide2.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QFileDialog, QButtonGroup, \
    QHBoxLayout, QInputDialog, QLineEdit
from PySide2.QtCore import Qt
from numpy import ndarray

from slicereg.gui.base import BaseQtView
from slicereg.gui.slider import LabelledSliderWidget


class SidebarView(BaseQtView):

    def __init__(self):

        self.widget = QWidget()

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        # Section Buttons
        # load_atlas_button = QPushButton("Load Atlas Tiff")
        # layout.addWidget(load_atlas_button)
        # load_atlas_button.clicked.connect(self.show_load_atlas_dialog)

        load_image_button = QPushButton("Load Section")
        layout.addWidget(load_image_button)
        load_image_button.clicked.connect(self.show_load_image_dialog)

        load_image_button2 = QPushButton("Quick Load Section")
        layout.addWidget(load_image_button2)
        load_image_button2.clicked.connect(lambda: self.load_section("data/RA_10X_scans/MeA/S1_07032020.ome.tiff"))

        # Scale Slider (Set Section Resolution)
        self.resample_widget = LabelledSliderWidget(min=15, max=200, label="Resample")
        layout.addLayout(self.resample_widget.layout)
        self.resample_widget.connect(lambda val: self.resample_section(val))

        self.resolution_widget = LabelledSliderWidget(min=1, max=100, label="Resolution")
        layout.addLayout(self.resolution_widget.layout)
        self.resolution_widget.connect(lambda val: self.transform_section(res=val))

        self.dim_widgets = []
        for dim in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
            widget = LabelledSliderWidget(min=-10000 if not dim.startswith('r') else -180, max=10000 if not dim.startswith('r') else 180, label=dim)
            layout.addLayout(widget.layout)
            fun = lambda d, value: self.transform_section(**{d: value})
            widget.connect(partial(fun, dim))
            self.dim_widgets.append((widget, fun))

        # Atlas BUttons
        button_hbox = QHBoxLayout()
        layout.addLayout(button_hbox)

        atlas_buttons = QButtonGroup(self.widget)
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

    @property
    def qt_widget(self) -> QWidget:
        return self.widget

    def on_section_loaded(self, image: ndarray, transform: ndarray, resolution_um: int) -> None:
        self.resolution_widget.set_value(resolution_um)

    def show_load_image_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Image",
            dir="../data/RA_10X_scans/MEA",
            filter="OME-TIFF (*.ome.tiff)"
        )
        if not filename:
            return
        self.load_section(filename=filename)

    def show_load_atlas_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Atlas File from Tiff Stack",
            dir=".",
            filter="TIFF (*.tif)"
        )
        if not filename:
            return
        self.load_atlas_from_file(filename=filename)

    def atlas_button_toggled(self, button: QPushButton, is_checked: bool):
        if not is_checked:  # Don't do anything for the button being unselected.
            return

        resolution_label = button.text()
        resolution = int("".join(filter(str.isdigit, resolution_label)))
        self.load_atlas(bgatlas_name=f"allen_mouse_{resolution}um")

    # Command Routing
    def load_section(self, filename: str):
        raise NotImplementedError("Connect to a LoadImageCommand before using.")

    def transform_section(self, **kwargs):
        raise NotImplementedError("Connect to UpdateSectionTransformCommand before using.")
    
    def resample_section(self, resolution_um: float):
        raise NotImplementedError("Connect to ResampleSectionCommand before using.")
        
    def load_atlas(self, bgatlas_name: str):
        raise NotImplementedError("Connect to LoadAtlasCommand before using.")

    def load_atlas_from_file(self, filename: str):
        raise NotImplementedError("Connect to LoadAtlasFromFileCommand before using.")

