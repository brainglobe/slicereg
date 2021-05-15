from unittest.mock import Mock

import numpy as np
import numpy.testing as npt
import pytest
from pytest import approx

from slicereg.app.app_model import AppModel, VolumeType
from slicereg.gui.volume_window import VolumeViewModel
from slicereg.utils import DependencyInjector


@pytest.fixture()
def app_model():
    app_model = AppModel(_injector=Mock(DependencyInjector))
    return app_model


@pytest.fixture()
def view_model(app_model):
    return VolumeViewModel(_model=app_model)


def test_volume_viewmodel_updates_section_transform_when_it_updates_in_the_app(app_model, view_model):
    app_model.section_transform = np.random.random(size=(4, 4))
    npt.assert_almost_equal(app_model.section_transform, view_model.section_transform)


def test_volume_viewmodel_updates_section_clim_when_section_image_updates_in_the_app(app_model,
                                                                                     view_model: VolumeViewModel):
    app_model.clim_3d = (0.5, 0.2)
    app_model.section_image = np.random.randint(0, 100, size=(10, 10), dtype=np.uint16)
    assert app_model.clim_3d_values == approx(view_model.clim)


def test_volume_viewmodel_updates_section_clim_when_clim_updates_in_the_app(app_model, view_model: VolumeViewModel):
    app_model.section_image = np.random.randint(0, 100, size=(10, 10), dtype=np.uint16)
    app_model.clim_3d = (0.5, 0.2)
    assert app_model.clim_3d_values == approx(view_model.clim)


def test_volume_viewmodel_updates_volume_when_registration_volume_loaded(app_model, view_model: VolumeViewModel):
    app_model.registration_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    npt.assert_almost_equal(app_model.registration_volume, view_model.atlas_volume)


def test_volume_viewmodel_updates_volume_when_switching_between_registration_volume_and_annotation_volume(app_model, view_model: VolumeViewModel):
    app_model.registration_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    app_model.annotation_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    app_model.visible_volume = VolumeType.REGISTRATION
    npt.assert_almost_equal(app_model.registration_volume, view_model.atlas_volume)

    app_model.visible_volume = VolumeType.ANNOTATION
    npt.assert_almost_equal(app_model.annotation_volume, view_model.atlas_volume)

    app_model.visible_volume = VolumeType.REGISTRATION
    npt.assert_almost_equal(app_model.registration_volume, view_model.atlas_volume)


def test_volume_viewmodel_updates_annotation_volume_when_visible_and_changes(app_model, view_model: VolumeViewModel):
    app_model.annotation_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    app_model.visible_volume = VolumeType.ANNOTATION
    npt.assert_almost_equal(app_model.annotation_volume, view_model.atlas_volume)

    app_model.annotation_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    npt.assert_almost_equal(app_model.annotation_volume, view_model.atlas_volume)


def test_volume_viewmodel_updates_registration_volume_when_visible_and_changes(app_model, view_model: VolumeViewModel):
    app_model.registration_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    app_model.visible_volume = VolumeType.REGISTRATION
    npt.assert_almost_equal(app_model.registration_volume, view_model.atlas_volume)

    app_model.annotation_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    npt.assert_almost_equal(app_model.registration_volume, view_model.atlas_volume)


def test_volume_viewmodel_describes_camera_parameters_for_3d_viewing(app_model, view_model: VolumeViewModel):
    app_model.registration_volume = np.random.randint(0, 100, size=(10, 10, 10), dtype=np.uint16)
    app_model.visible_volume = VolumeType.REGISTRATION

    # Camera look-at position
    x, y, z = view_model.camera_center
    assert isinstance(x, float) and isinstance(y, float) and isinstance(z, float)

    # Camera distance from look-at position
    assert isinstance(view_model.camera_distance, float)


def test_volume_viewmodel_describes_volume_clim(view_model: VolumeViewModel):
    c_min, c_max = view_model.volume_clim
    assert isinstance(c_min, int) and isinstance(c_max, int)
