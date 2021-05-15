from dataclasses import dataclass, field
from typing import Optional, Tuple, List, Any, Callable

from slicereg.app.app_model import AppModel, VolumeType
from slicereg.utils.observable import HasObservableAttributes


@dataclass(unsafe_hash=True)
class SidebarViewModel(HasObservableAttributes):
    _model: AppModel = field(hash=False)
    selected_bgatlas: Optional[str] = None
    _atlas_resolution_text: str = ''
    bgatlas_dropdown_entries: List[str] = field(default_factory=list)
    _section_resolution_text: str = ''

    def __post_init__(self):
        HasObservableAttributes.__init__(self)
        self._model.register(self.update)

    def update(self, changed: str):
        update_funs = {
            'bgatlas_names': self._update_bgatlas_dropdown_list,
            'section_image_resolution': self._update_section_resolution_text,
        }
        if (fun := update_funs.get(changed)) is not None:
            fun()

    def _update_bgatlas_dropdown_list(self):
        self.bgatlas_dropdown_entries = self._model.bgatlas_names

    def _update_section_resolution_text(self):
        res = self._model.section_image_resolution
        if res is None:
            text = ''
        elif int(res) == float(res):
            text = str(int(res))
        else:
            text = str(float(res))
        self._section_resolution_text = text

    @property
    def section_resolution_text(self) -> str:
        return self._section_resolution_text

    @section_resolution_text.setter
    def section_resolution_text(self, text: str):
        # Validate: is float
        try:
            if text:
                self._model.section_image_resolution = float(text)
            else:
                self._model.section_image_resolution = None
        except ValueError:
            self._section_resolution_text = self._section_resolution_text
            return

    def click_coronal_button(self):
        self._model.orient_section_to_coronal()

    def click_sagittal_button(self):
        self._model.orient_section_to_sagittal()

    def click_axial_button(self):
        self._model.orient_section_to_axial()

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
        self._model.load_atlas_from_file(filename=filename, resolution_um=int(self.atlas_resolution_text))

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

    @property
    def atlas_resolution_text(self) -> str:
        return self._atlas_resolution_text

    @atlas_resolution_text.setter
    def atlas_resolution_text(self, text: str):
        self._atlas_resolution_text = text if text.isdigit() or not text else self._atlas_resolution_text

    def click_registration_atlas_selector_button(self):
        self._model.visible_volume = VolumeType.REGISTRATION

    def click_annotation_atlas_selector_button(self):
        self._model.visible_volume = VolumeType.ANNOTATION
