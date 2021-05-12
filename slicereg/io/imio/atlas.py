from typing import Optional

import imio

from slicereg.commands.base import BaseLocalAtlasReader
from slicereg.core.atlas import Atlas


class ImioLocalAtlasReader(BaseLocalAtlasReader):

    def read(self, filename: str, resolution_um: float) -> Atlas:

        volume = imio.load_any(filename)

        return Atlas(
            volume=volume,
            resolution_um=resolution_um,
        )