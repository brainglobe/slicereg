from slicereg.gui.app_model import AppModel
from unittest.mock import Mock
from slicereg.utils import DependencyInjector
from slicereg.commands.load_section import LoadSectionCommand, LoadImageData
from result import Ok
from uuid import uuid4
import numpy

def test_load_section_appends_new_section_and_updates_current_section_id():
    DI = Mock(DependencyInjector)
    load_section = Mock(LoadSectionCommand)
    load_section.return_value = Ok(LoadImageData(
        section_id=uuid4(),
        section_image=numpy.empty([4,4]), 
        resolution_um = 200, 
        num_channels = 1
    ))

    DI.build.return_value = load_section
    model = AppModel(_injector=DI)
    model.update_section = Mock()
    model.load_section(filename='data.tiff')
    
    assert len(model.loaded_sections) == 1

    model.load_section(filename='data2.tiff')

    assert len(model.loaded_sections) == 2