from dataclasses import dataclass, field
from typing import Optional, Tuple, List

from slicereg.commands.utils import Signal
from slicereg.gui.app_model import AppModel, VolumeType


@dataclass(unsafe_hash=True)
class SidebarViewModel:
    _model: AppModel = field(hash=False)
    selected_bgatlas: Optional[str] = None
    loadatlas_resolution: Optional[int] = None
    updated: Signal = field(default_factory=Signal)

    def __post_init__(self):
        self._model.updated.connect(self.update)

    def update(self, **kwargs):
        self.updated.emit(**kwargs)

    @property
    def clim_2d(self) -> Tuple[float, float]:
        return self._model.clim_2d

    @property
    def clim_3d(self) -> Tuple[float, float]:
        return self._model.clim_3d

    @property
    def bgatlas_names(self) -> List[str]:
        return self._model.bgatlas_names

    def update_section_resolution_textbox(self, resolution: str) -> None:
        self._model.section_image_resolution = float(resolution)

    def click_coronal_button(self):
        self._model.update_section(rx=0, ry=0, rz=-90)

    def click_sagittal_button(self):
        self._model.update_section(rx=90, ry=0, rz=-90)

    def click_axial_button(self):
        self._model.update_section(rx=0, ry=90, rz=-90)

    def move_clim_slice_slider(self, values: Tuple[int, int]):
        self._model.clim_2d = values

    def move_clim_volume_slider(self, values: Tuple[int, int]):
        self._model.clim_3d = values

    def click_quick_load_section_button(self):
        self._model.load_section("data/RA_10X_scans/MeA/S1_07032020.ome.tiff")

    def slide_resample_slider(self, val: int):
        self._model.resample_section(val)

    def slide_resolution_slider(self, val: int):
        self._model.update_section(res=val)

    def click_update_bgatlas_list_button(self):
        self._model.list_bgatlases()

    def submit_load_atlas_from_file(self, filename: str):
        if self.loadatlas_resolution is None:
            return
        self._model.load_atlas_from_file(filename=filename, resolution_um=self.loadatlas_resolution)

    def click_load_bgatlas_button(self):
        self._model.load_bgatlas(name=self.selected_bgatlas)

    def change_bgatlas_selection_dropdown(self, text: str):
        self.selected_bgatlas = text

    def submit_load_section_from_file(self, filename: str):
        self._model.load_section(filename=filename)

    def change_x_slider(self, value: int):
        self._model.update_section(x=value)

    def change_y_slider(self, value: int):
        self._model.update_section(y=value)

    def change_z_slider(self, value: int):
        self._model.update_section(z=value)

    def change_rotx_slider(self, value: int):
        self._model.update_section(rx=value)

    def change_roty_slider(self, value: int):
        self._model.update_section(ry=value)

    def change_rotz_slider(self, value: int):
        self._model.update_section(rz=value)

    def update_resolution_textbox(self, text: str):
        self.loadatlas_resolution = int(text)

    def click_registration_atlas_selector_button(self):
        self._model.visible_volume = VolumeType.REGISTRATION

    def click_annotation_atlas_selector_button(self):
        self._model.visible_volume = VolumeType.ANNOTATION
