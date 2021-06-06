from unittest.mock import Mock

import numpy as np

from slicereg.commands.base import BaseRepo, BaseLocalImageReader, ImageReaderData
from slicereg.commands.load_section import LoadSectionCommand
from slicereg.io.tifffile.ome_image import OmeTiffImageReader


def test_load_section_command_gets_section_image_from_file():
    reader = Mock(BaseLocalImageReader)
    reader.read.return_value = ImageReaderData(channels=np.empty((2, 4, 4)), resolution_um=1.4)
    repo = Mock(BaseRepo)

    load_section = LoadSectionCommand(_repo=repo, _image_reader=reader)
    result = load_section(filename="myfile.tiff")
    assert reader.read.called_with(filename="myfile.tiff")
    assert result.ok().section_image.ndim == 2


def test_load_section_returns_section_id():
    reader = Mock(BaseLocalImageReader)
    reader.read.return_value = ImageReaderData(channels=np.empty((2, 4, 4)), resolution_um=1.4)
    repo = Mock(BaseRepo)
    load_section = LoadSectionCommand(_repo=repo, _image_reader=reader)
    result = load_section(filename="myfile.tiff")
    assert result.ok().section_id


def test_load_section_command_is_okay_with_quicknii_xml_files():
    load_section = LoadSectionCommand(_repo=Mock(BaseRepo), _image_reader=OmeTiffImageReader())
    result = load_section(filename="data/deepslice_output/results_S2_07032020_downsampled.xml")
    assert result.ok()
