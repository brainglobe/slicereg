from functools import partial
from typing import List

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QLineEdit, QHBoxLayout, QLabel
from numpy import ndarray

from slicereg.gui.base import BaseQtView
from slicereg.gui.commands import CommandProvider
from slicereg.gui.slider import LabelledSliderWidget


class SidebarView(BaseQtView):

    def __init__(self, commands: CommandProvider):

        self.commands = commands
        self.widget = QWidget()

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        # Load atlas button + resolution textbox
        load_atlas_layout = QHBoxLayout()

        load_atlas_layout.addWidget(QLabel(text='Res (μm):'))

        self.resolution_textbox = QLineEdit()
        load_atlas_layout.addWidget(self.resolution_textbox)

        load_atlas_button = QPushButton("Load Atlas File")
        load_atlas_layout.addWidget(load_atlas_button)
        load_atlas_button.clicked.connect(self.show_load_atlas_dialog)

        layout.addLayout(load_atlas_layout)

        # Section Buttons
        list_atlas_button = QPushButton("Update Brainglobe Atlases")
        layout.addWidget(list_atlas_button)
        list_atlas_button.clicked.connect(lambda: self.commands.list_bgatlases())

        self.list_atlas_dropdown = QComboBox()
        layout.addWidget(self.list_atlas_dropdown)

        load_atlas_button = QPushButton("Load Atlas")
        layout.addWidget(load_atlas_button)
        load_atlas_button.clicked.connect(self._load_atlas)

        load_image_button = QPushButton("Load Section")
        layout.addWidget(load_image_button)
        load_image_button.clicked.connect(self.show_load_image_dialog)

        load_image_button2 = QPushButton("Quick Load Section")
        layout.addWidget(load_image_button2)
        load_image_button2.clicked.connect(lambda: self.commands.load_section("data/RA_10X_scans/MeA/S1_07032020.ome.tiff"))

        # Scale Slider (Set Section Resolution)
        self.resample_widget = LabelledSliderWidget(min=15, max=200, label="Resample")
        layout.addLayout(self.resample_widget.layout)
        self.resample_widget.connect(lambda val: self.commands.resample_section(val))

        self.resolution_widget = LabelledSliderWidget(min=1, max=100, label="Resolution")
        layout.addLayout(self.resolution_widget.layout)
        self.resolution_widget.connect(lambda val: self.commands.update_section(res=val))

        self.dim_widgets = []
        for dim in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
            widget = LabelledSliderWidget(min=-10000 if not dim.startswith('r') else -180, max=10000 if not dim.startswith('r') else 180, label=dim)
            layout.addLayout(widget.layout)
            fun = lambda d, value: self.commands.update_section(**{d: value})
            widget.connect(partial(fun, dim))
            self.dim_widgets.append((widget, fun))

        coronal_button = QPushButton("Coronal")
        coronal_button.clicked.connect(lambda: self.commands.update_section(rx=0, ry=0, rz=-90))
        sagittal_button = QPushButton("Sagittal")
        sagittal_button.clicked.connect(lambda: self.commands.update_section(rx=90, ry=0, rz=-90))
        axial_button = QPushButton("Axial")
        axial_button.clicked.connect(lambda: self.commands.update_section(rx=0, ry=90, rz=-90))

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(coronal_button)
        buttons_layout.addWidget(sagittal_button)
        buttons_layout.addWidget(axial_button)
        layout.addLayout(buttons_layout)

    @property
    def qt_widget(self) -> QWidget:
        return self.widget

    def show_load_image_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Image",
            dir="../data/RA_10X_scans/MEA",
            filter="OME-TIFF (*.ome.tiff)"
        )
        if not filename:
            return
        self.commands.load_section(filename=filename)

    def show_load_atlas_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Atlas from File",
            dir=".",
            filter="Image Files (*.tif *.tiff *.nii)"
        )
        if not filename:
            return
        resolution_um = int(self.resolution_textbox.text())
        self.commands.load_atlas_from_file(filename=filename, resolution_um=resolution_um)

    def show_brainglobe_atlases(self, atlas_names: List[str]):
        self.list_atlas_dropdown.addItems(atlas_names)

    def _load_atlas(self):
        selected_atlas = self.list_atlas_dropdown.currentText()
        print(f"Loading Atlas: {selected_atlas}")
        self.commands.load_atlas(bgatlas_name=selected_atlas)
