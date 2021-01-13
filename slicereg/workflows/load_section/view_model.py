from dataclasses import dataclass, field
from typing import List

from slicereg.workflows.load_section.workflow import BasePresenter, LoadSectionResponse


@dataclass
class LoadImageViewModel:
    sections: List[LoadSectionResponse] = field(default_factory=list)


class LoadImagePresenter(BasePresenter):

    def __init__(self, model: LoadImageViewModel):
        self._model = model

    def show(self, data: LoadSectionResponse):
        self._model.sections.append(data)
