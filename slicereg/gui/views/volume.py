from __future__ import annotations

from PySide2.QtWidgets import QWidget
from numpy import array
from vispy.scene import SceneCanvas, ViewBox, Volume, Image, ArcballCamera
from vispy.visuals import filters
from vispy.visuals.transforms import MatrixTransform

from slicereg.gui.view_models.volume import VolumeViewModel
from slicereg.gui.views.base import BaseQtWidget, BaseView


class VolumeView(BaseQtWidget, BaseView):

    def __init__(self):
        super().__init__()
        self._canvas = SceneCanvas()

        self._viewbox = ViewBox(parent=self._canvas.scene)
        self._canvas.central_widget.add_widget(self._viewbox)
        self._viewbox.camera = ArcballCamera(fov=0)

        self._atlas_volume = Volume(array([[[1, 2]]]) * 1000, parent=self._viewbox.scene)  # , interpolation='nearest')
        self._atlas_volume.attach(filters.ColorFilter((1., .5, 0., 1.)))
        self._atlas_volume.set_gl_state('additive', depth_test=False)

        self._section_image = Image(parent=self._viewbox.scene, cmap='grays')
        self._section_image.attach(filters.ColorFilter((0., .5, 1., 1.)))
        self._section_image.set_gl_state('additive', depth_test=False)

    def on_registration(self, model):
        self._canvas.events.key_press.connect(lambda event: model.press_key(event.key.name))

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def update(self, model: VolumeViewModel, changed: str, **kwargs) -> None:
        render_funs = {
            'atlas_volume': self._render_volume,
            'section_image': self._render_section,
            'section_transform': self._render_section_transform,
            'clim': self._render_section_clim,
        }
        render_funs[changed](model=model)

    def _render_section_clim(self, model: VolumeViewModel) -> None:
        self._section_image.clim = model.clim
        self._canvas.update()

    def _render_section_transform(self, model: VolumeViewModel) -> None:
        self._section_image.transform = MatrixTransform(model.section_transform.T)
        self._canvas.update()

    def _render_section(self, model: VolumeViewModel) -> None:
        self._section_image.set_data(model.section_image.T)
        self._canvas.update()

    def _render_volume(self, model: VolumeViewModel) -> None:
        self._atlas_volume.set_data(model.atlas_volume.swapaxes(0, 2), clim=model.volume_clim)
        self._viewbox.camera.center = model.camera_center
        self._viewbox.camera.scale_factor = model.camera_distance
        self._canvas.update()
