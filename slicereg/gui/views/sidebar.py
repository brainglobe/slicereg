from __future__ import annotations

from dataclasses import field, dataclass
from functools import partial
from typing import List, Tuple

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QLineEdit, QHBoxLayout, QLabel

from slicereg.commands.utils import Signal
from slicereg.gui.views.base import BaseQtView
from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.views.slider import LabelledSliderWidget
from vendor.napari_qrange_slider.qt_range_slider import QHRangeSlider


class SidebarView(BaseQtView):

    def __init__(self, model: SidebarViewModel):

        self.widget = QWidget()

        self.model = model
        self.model.updated.connect(self.update)

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
        list_atlas_button.clicked.connect(lambda: self.model._commands.list_bgatlases())

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
        load_image_button2.clicked.connect(
            lambda: self.model._commands.load_section("data/RA_10X_scans/MeA/S1_07032020.ome.tiff"))

        # Scale Slider (Set Section Resolution)
        self.resample_widget = LabelledSliderWidget(min=15, max=200, label="Resample")
        layout.addLayout(self.resample_widget.layout)
        self.resample_widget.connect(lambda val: self.model._commands.resample_section(val))

        self.resolution_widget = LabelledSliderWidget(min=1, max=100, label="Resolution")
        layout.addLayout(self.resolution_widget.layout)
        self.resolution_widget.connect(lambda val: self.model._commands.update_section(res=val))

        self.dim_widgets = []
        for dim in ['x', 'y', 'z', 'rx', 'ry', 'rz']:
            widget = LabelledSliderWidget(min=-10000 if not dim.startswith('r') else -180,
                                          max=10000 if not dim.startswith('r') else 180, label=dim)
            layout.addLayout(widget.layout)
            fun = lambda d, value: self.model._commands.update_section(**{d: value})
            widget.connect(partial(fun, dim))
            self.dim_widgets.append((widget, fun))

        coronal_button = QPushButton(self.model.coronal_button_label)
        coronal_button.clicked.connect(lambda: self.model.click_coronal_button())
        sagittal_button = QPushButton(self.model.sagittal_button_label)
        sagittal_button.clicked.connect(lambda: self.model.click_sagittal_button())
        axial_button = QPushButton(self.model.axial_button_label)
        axial_button.clicked.connect(lambda: self.model.click_axial_button())

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(coronal_button)
        buttons_layout.addWidget(sagittal_button)
        buttons_layout.addWidget(axial_button)
        layout.addLayout(buttons_layout)

        slice_clim_slider = QHRangeSlider(initial_values=(0., 1.), data_range=(0., 1.), step_size=0.01)
        slice_clim_slider.valuesChanged.connect(lambda values: self.model.move_clim_slice_slider(values))
        layout.addWidget(slice_clim_slider)

        volume_slice_clim_slider = QHRangeSlider(initial_values=(0., 1.), data_range=(0., 1.), step_size=0.01)
        volume_slice_clim_slider.valuesChanged.connect(lambda values: self.model.move_clim_volume_slider(values))
        layout.addWidget(volume_slice_clim_slider)

    @property
    def qt_widget(self) -> QWidget:
        return self.widget

    def update(self) -> None:
        self.list_atlas_dropdown.addItems(self.model.bgatlas_names)

    def show_load_image_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Image",
            dir="../../../data/RA_10X_scans/MeA",
            filter="OME-TIFF (*.ome.tiff)"
        )
        if not filename:
            return
        self.model._commands.load_section(filename=filename)

    def show_load_atlas_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Atlas from File",
            dir="..",
            filter="Image Files (*.tif *.tiff *.nii)"
        )
        if not filename:
            return
        resolution_um = int(self.resolution_textbox.text())
        self.model._commands.load_atlas_from_file(filename=filename, resolution_um=resolution_um)

    def _load_atlas(self):
        selected_atlas = self.list_atlas_dropdown.currentText()
        print(f"Loading Atlas: {selected_atlas}")
        self.model._commands.load_atlas(bgatlas_name=selected_atlas)


@dataclass
class SidebarViewModel:
    _model: AppModel = field(repr=False)
    _commands: CommandProvider = field(repr=False)
    updated: Signal = field(default_factory=Signal, repr=False)
    coronal_button_label: str = "Coronal"
    sagittal_button_label: str = "Sagittal"
    axial_button_label: str = "Axial"

    def __post_init__(self):
        self._model.updated.connect(self.update)
        self.update()

    def update(self):
        self.updated.emit()

    @property
    def clim_2d(self) -> Tuple[float, float]:
        return self._model.clim_2d

    @property
    def clim_3d(self) -> Tuple[float, float]:
        return self._model.clim_3d

    @property
    def bgatlas_names(self) -> List[str]:
        return self._model.bgatlas_names

    def click_coronal_button(self):
        self._commands.update_section(rx=0, ry=0, rz=-90)

    def click_sagittal_button(self):
        self._commands.update_section(rx=90, ry=0, rz=-90)

    def click_axial_button(self):
        self._commands.update_section(rx=0, ry=90, rz=-90)

    def move_clim_slice_slider(self, values: Tuple[int, int]):
        self._model.update(clim_2d=values)

    def move_clim_volume_slider(self, values: Tuple[int, int]):
        self._model.update(clim_3d=values)
