from pathlib import Path
from typing import Optional

import imio

from slicereg.commands.base import BaseLocalAtlasReader, AtlasReaderData


class ImioLocalAtlasReader(BaseLocalAtlasReader):

    def read(self, filename: str) -> Optional[AtlasReaderData]:
        path = Path(filename)
        volume = imio.load_any(str(path))

        return AtlasReaderData(
            source="File",
            name=path.name,
            registration_volume=volume,
            annotation_volume=None,
            resolution_um=None,
        )