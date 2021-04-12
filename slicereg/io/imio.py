import imio

from slicereg.models.atlas import Atlas


class ImioAtlasReader:

    @staticmethod
    def read(path: str, resolution_um: int) -> Atlas:
        # TODO: can support scaling, parallel loading, map to coordinate space (anterior, left, superior, etc.)
        volume = imio.load_any(path)

        return Atlas(
            volume=volume,
            resolution_um=resolution_um,
        )
