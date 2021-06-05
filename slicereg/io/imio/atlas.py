from pathlib import Path
from typing import Optional

import imio

from slicereg.commands.base import BaseLocalAtlasReader, RemoteAtlasReaderData
from slicereg.commands.base.atlas_reader import LocalAtlasReaderData


class ImioLocalAtlasReader(BaseLocalAtlasReader):

    def read(self, filename: str) -> Optional[LocalAtlasReaderData]:
        path = Path(filename)
        volume = imio.load_any(str(path))

        return LocalAtlasReaderData(
            source="File",
            name=path.name,
            registration_volume=volume,
        )
