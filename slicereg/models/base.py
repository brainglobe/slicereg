from abc import ABC
from dataclasses import is_dataclass, replace


class FrozenUpdater(ABC):

    def update(self, **kwargs):
        assert is_dataclass(self), "only works on dataclasses."
        return replace(self, **kwargs)