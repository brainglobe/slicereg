from __future__ import annotations

import numpy as np
from PySide2.QtWidgets import QWidget
from numpy import array
from vispy.scene import SceneCanvas, ViewBox, Volume, Image, ArcballCamera
from vispy.visuals import filters
from vispy.visuals.transforms import MatrixTransform

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
        self._canvas.events.key_press.connect(lambda event: model.on_key_press(event.key.name))

    @property
    def qt_widget(self) -> QWidget:
        return self._canvas.native

    def update(self, **kwargs) -> None:
        if kwargs.get('atlas_volume') is not None:
            self._atlas_volume.set_data(kwargs['atlas_volume'], clim=kwargs['volume_clim'])
            self._viewbox.camera.center = kwargs['camera_center']
            self._viewbox.camera.scale_factor = kwargs['camera_distance']

        if (image := kwargs.get('section_image')) is not None:
            self._section_image.set_data(image)

        if (transform := kwargs.get('section_transform')) is not None:
            self._section_image.transform = MatrixTransform(transform)

        if (clim := kwargs.get('clim')) is not None:
            self._section_image.clim = clim

        self._canvas.update()
