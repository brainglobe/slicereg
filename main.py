from src.gui.presenter import Presenter
from src.gui.window import Window
from src.gui.workflows import WorkflowProvider
from src.repos.inmemory import InMemoryRepo
from src.serializers.bg_atlas import BGAtlasSerializer
from src.serializers.ome_tiff import OmeTiffSerializer

win = Window(title="Registration App")

presenter = Presenter(win=win)
repo = InMemoryRepo()

use_cases = WorkflowProvider(
    section_repo=repo,
    atlas_repo=repo,
    section_serializer=OmeTiffSerializer(),
    atlas_serializer=BGAtlasSerializer(),
    load_atlas_presenter=presenter,
    select_channel_presenter=presenter,
    load_section_presenter=presenter,
    move_section_presenter=presenter,
)
win.register_use_cases(app=use_cases)
win.run()
