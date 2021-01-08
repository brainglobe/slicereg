from src.core.load_atlas.load_atlas import LoadAtlasWorkflow
from src.core.load_atlas.repo import AtlasRepo
from src.core.load_section.load_section import LoadSectionWorkflow
from src.core.load_section.repo import SectionRepo
from src.core.select_channel.select_channel import SelectChannelWorkflow
from src.gui.presenter import Presenter
from src.gui.window import Window
from src.gui.workflows import WorkflowProvider
from src.core.load_atlas.io import BGAtlasSerializer
from src.core.load_section.io import OmeTiffSerializer

win = Window(title="Registration App")

presenter = Presenter(win=win)
repo = SectionRepo(
    serializer=OmeTiffSerializer()
)

use_cases = WorkflowProvider(
    section_repo=repo,
    load_atlas=LoadAtlasWorkflow(
        repo=AtlasRepo(
            serializer=BGAtlasSerializer()
        ),
        presenter=presenter,
    ),
    load_section=LoadSectionWorkflow(
        repo=repo,
        presenter=presenter,
    ),
    select_channel=SelectChannelWorkflow(
        repo=repo,
        presenter=presenter,
    ),
    move_section_presenter=presenter,
)
win.register_use_cases(app=use_cases)
win.run()


# events, renderer = Widget()  # Displays things onscreen and takes input from user.

# events.on_callback(         # Takes input from user and packs into data
#     Controller(             # Unpacks data from events and sends to usecases
#         UseCase(            # Creates entities, does script
#             Repo(
#                 Serializer  # Gets data from a file format
#             ),              # Gets data
#             Presenter(      # Gives data to the renderer
#                 renderer    # Puts the data onscreen (Specific to platform)
#             ),
#         )
#     )
# )


# events, renderer = Widget()  # Displays things onscreen and takes input from user.

# events.on_callback(         # Takes input from user and packs into data
#     Controller(             # Unpacks data from events and sends to usecases
#         UseCase(            # Creates entities, does script
#             Repo(
#                 Serializer  # Gets data from a file format
#             ),              # Gets data
#             Presenter(      # Gives data to the renderer
#                 renderer    # Puts the data onscreen (Specific to platform)
#             ),
#         )
#     )
# )