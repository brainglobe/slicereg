from src.gui.presenter import LoadAtlasPresenter, LoadSectionPresenter, SelectChannelPresenter
from src.gui.window import Window
from src.gui.workflows import ViewModel
from src.repos.bgatlas_repo import BrainglobeAtlasRepo
from src.workflows.load_atlas import LoadAtlasWorkflow
from src.workflows.load_section.io import OmeTiffSerializer
from src.workflows.load_section.load_section import LoadSectionWorkflow
from src.workflows.load_section.repo import SectionRepo
from src.workflows.move_section import MoveSectionWorkflow
from src.workflows.select_channel import SelectChannelWorkflow

win = Window(title="Registration App")

repo = SectionRepo(
    serializer=OmeTiffSerializer()
)

use_cases = ViewModel(
    win=win,
    load_atlas=LoadAtlasWorkflow(
        repo=BrainglobeAtlasRepo(),
        presenter=LoadAtlasPresenter(win=win),
    ),
    load_section=LoadSectionWorkflow(
        repo=repo,
        presenter=LoadSectionPresenter(win=win),
    ),
    select_channel=SelectChannelWorkflow(
        repo=repo,
        presenter=SelectChannelPresenter(win=win),
    ),
    _move_section=MoveSectionWorkflow(
        repo=repo,
    )
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