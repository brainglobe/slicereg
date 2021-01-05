from src.gui.workflows import WorkflowProvider
from src.gui.window import Window
from src.gui.presenter import Presenter
from src.repos.inmemory_atlas import InMemoryAtlasRepo
from src.repos.inmemory_section import InMemorySectionRepo
from src.serializers.ome_tiff import OmeTiffSerializer

win = Window(title="Registration App")

presenter = Presenter(win=win)
use_cases = WorkflowProvider(
    section_repo=InMemorySectionRepo(),
    atlas_repo=InMemoryAtlasRepo(),
    section_serializer=OmeTiffSerializer(),
    load_atlas_presenter=presenter,
    select_channel_presenter=presenter,
    load_section_presenter=presenter,
    move_section_presenter=presenter,
)
win.register_use_cases(app=use_cases)
win.run()
