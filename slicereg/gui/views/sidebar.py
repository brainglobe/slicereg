from __future__ import annotations

from dataclasses import field, dataclass
from functools import partial
from typing import List, Tuple, Optional

from PySide2.QtWidgets import QWidget, QVBoxLayout, QPushButton, QFileDialog, QComboBox, QLineEdit, QHBoxLayout, QLabel

from slicereg.commands.utils import Signal
from slicereg.gui.views.base import BaseQtWidget
from slicereg.gui.commands import CommandProvider
from slicereg.gui.model import AppModel
from slicereg.gui.views.slider import LabelledSliderWidget
from vendor.napari_qrange_slider.qt_range_slider import QHRangeSlider


class SidebarView(BaseQtWidget):

    def __init__(self, model: SidebarViewModel):

        self.widget = QWidget()

        self.model = model
        self.model.updated.connect(self.update)

        layout = QVBoxLayout()
        self.widget.setLayout(layout)

        # Load atlas controls
        load_atlas_layout = QHBoxLayout()

        load_atlas_layout.addWidget(QLabel(text='Res (μm):'))

        self.resolution_textbox = QLineEdit()
        load_atlas_layout.addWidget(self.resolution_textbox)
        self.resolution_textbox.textEdited.connect(lambda text: self.model.update_resolution_textbox(text=text))

        load_atlas_button = QPushButton("Load Atlas File")
        load_atlas_layout.addWidget(load_atlas_button)
        load_atlas_button.clicked.connect(self.show_load_atlas_dialog)

        layout.addLayout(load_atlas_layout)

        list_atlas_button = QPushButton("Update Brainglobe Atlases")
        layout.addWidget(list_atlas_button)
        list_atlas_button.clicked.connect(lambda: self.model.click_update_bgatlas_list_button())

        self.list_atlas_dropdown = QComboBox()
        layout.addWidget(self.list_atlas_dropdown)
        self.list_atlas_dropdown.currentTextChanged.connect(lambda text: self.model.change_bgatlas_selection_dropdown(text=text))

        load_atlas_button = QPushButton("Load Atlas")
        layout.addWidget(load_atlas_button)
        load_atlas_button.clicked.connect(lambda: self.model.click_load_bgatlas_button())

        # Load Section Buttons
        load_image_button = QPushButton("Load Section")
        layout.addWidget(load_image_button)
        load_image_button.clicked.connect(self.show_load_image_dialog)

        load_image_button2 = QPushButton("Quick Load Section")
        layout.addWidget(load_image_button2)
        load_image_button2.clicked.connect(lambda: self.model.click_quick_load_section_button())

        # Scale Sliders (Set Section Resolution)
        self.resample_widget = LabelledSliderWidget(min=15, max=200, label="Resample")
        layout.addLayout(self.resample_widget.layout)
        self.resample_widget.connect(lambda val: self.model.slide_resample_slider(val=val))

        self.resolution_widget = LabelledSliderWidget(min=1, max=100, label="Resolution")
        layout.addLayout(self.resolution_widget.layout)
        self.resolution_widget.connect(lambda val: self.model.slide_resolution_slider(val=val))

        # Movement Sliders
        self.x_slider = LabelledSliderWidget(min=-10000, max=10000, label='x')
        layout.addLayout(self.x_slider.layout)
        self.x_slider.connect(lambda val: self.model.change_x_slider(value=val))

        self.y_slider = LabelledSliderWidget(min=-10000, max=10000, label='y')
        layout.addLayout(self.y_slider.layout)
        self.y_slider.connect(lambda val: self.model.change_y_slider(value=val))

        self.z_slider = LabelledSliderWidget(min=-10000, max=10000, label='z')
        layout.addLayout(self.z_slider.layout)
        self.z_slider.connect(lambda val: self.model.change_z_slider(value=val))

        self.rotx_slider = LabelledSliderWidget(min=-180, max=180, label='rotx')
        layout.addLayout(self.rotx_slider.layout)
        self.rotx_slider.connect(lambda val: self.model.change_rotx_slider(value=val))

        self.roty_slider = LabelledSliderWidget(min=-180, max=180, label='roty')
        layout.addLayout(self.roty_slider.layout)
        self.roty_slider.connect(lambda val: self.model.change_roty_slider(value=val))

        self.rotz_slider = LabelledSliderWidget(min=-180, max=180, label='rotz')
        layout.addLayout(self.rotz_slider.layout)
        self.rotz_slider.connect(lambda val: self.model.change_rotz_slider(value=val))

        # Quick-rotation buttons
        buttons_layout = QHBoxLayout()

        coronal_button = QPushButton(self.model.coronal_button_label)
        coronal_button.clicked.connect(lambda: self.model.click_coronal_button())
        buttons_layout.addWidget(coronal_button)

        sagittal_button = QPushButton(self.model.sagittal_button_label)
        sagittal_button.clicked.connect(lambda: self.model.click_sagittal_button())
        buttons_layout.addWidget(sagittal_button)

        axial_button = QPushButton(self.model.axial_button_label)
        axial_button.clicked.connect(lambda: self.model.click_axial_button())
        buttons_layout.addWidget(axial_button)

        layout.addLayout(buttons_layout)

        # clim sliders
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
        self.list_atlas_dropdown.addItems(self.model.bgatlas_names)  # todo: if called multiple times, will append the same items again.

    def show_load_image_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Image",
            dir="../../../data/RA_10X_scans/MeA",
            filter="OME-TIFF (*.ome.tiff)"
        )
        if not filename:
            return
        self.model.submit_load_section_from_file(filename=filename)

    def show_load_atlas_dialog(self):
        filename, filetype = QFileDialog.getOpenFileName(
            parent=self.qt_widget,
            caption="Load Atlas from File",
            dir="..",
            filter="Image Files (*.tif *.tiff *.nii)"
        )
        if not filename:
            return
        self.model.submit_load_atlas_from_file(filename=filename)


@dataclass
class SidebarViewModel:
    _model: AppModel = field(repr=False)
    _commands: CommandProvider = field(repr=False)
    updated: Signal = field(default_factory=Signal, repr=False)
    coronal_button_label: str = "Coronal"
    sagittal_button_label: str = "Sagittal"
    axial_button_label: str = "Axial"
    selected_bgatlas: Optional[str] = None
    loadatlas_resolution: Optional[int] = None

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

    def click_quick_load_section_button(self):
        self._commands.load_section("data/RA_10X_scans/MeA/S1_07032020.ome.tiff")

    def slide_resample_slider(self, val: int):
        self._commands.resample_section(val)

    def slide_resolution_slider(self, val: int):
        self._commands.update_section(res=val)

    def click_update_bgatlas_list_button(self):
        self._commands.list_bgatlases()

    def submit_load_atlas_from_file(self, filename: str):
        if self.loadatlas_resolution is None:
            return
        self._commands.load_atlas_from_file(filename=filename, resolution_um=self.loadatlas_resolution)

    def click_load_bgatlas_button(self):
        print(f"Loading Atlas: {self.selected_bgatlas}")
        self._commands.load_atlas(bgatlas_name=self.selected_bgatlas)

    def change_bgatlas_selection_dropdown(self, text: str):
        self.selected_bgatlas = text

    def submit_load_section_from_file(self, filename: str):
        self._commands.load_section(filename=filename)

    def change_x_slider(self, value: int):
        self._commands.update_section(x=value)

    def change_y_slider(self, value: int):
        self._commands.update_section(y=value)

    def change_z_slider(self, value: int):
        self._commands.update_section(z=value)

    def change_rotx_slider(self, value: int):
        self._commands.update_section(rx=value)

    def change_roty_slider(self, value: int):
        self._commands.update_section(ry=value)

    def change_rotz_slider(self, value: int):
        self._commands.update_section(rz=value)

    def update_resolution_textbox(self, text: str):
        self.loadatlas_resolution = int(text)
