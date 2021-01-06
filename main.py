from src.core.atlas.repos import AtlasRepo
from src.gui.presenter import Presenter
from src.gui.window import Window
from src.gui.workflows import WorkflowProvider
from src.core.models.section import SectionRepo
from src.core.atlas.io import BGAtlasSerializer
from src.core.section.io import OmeTiffSerializer

win = Window(title="Registration App")

presenter = Presenter(win=win)
repo = SectionRepo()

use_cases = WorkflowProvider(
    section_repo=repo,
    atlas_repo=AtlasRepo(),
    section_serializer=OmeTiffSerializer(),
    atlas_serializer=BGAtlasSerializer(),
    load_atlas_presenter=presenter,
    select_channel_presenter=presenter,
    load_section_presenter=presenter,
    move_section_presenter=presenter,
)
win.register_use_cases(app=use_cases)
win.run()
