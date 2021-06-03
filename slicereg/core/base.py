from abc import ABC
from dataclasses import is_dataclass, replace


class FrozenUpdater(ABC):

    def update(self, **kwargs):
        """
        Returns a new object with updated attributes.  If '__' is used, can update a nested attribute.

        Examples:
            >>> from dataclasses import dataclass
            >>> from typing import Any
            >>> @dataclass(frozen=True)
            ... class Object(FrozenUpdater):
            ...    x: Any = 0
            ...    y: Any = 0
            ...    z: Any = 0
            >>> obj = Object(x=0, y=0, z=0)
            >>> obj.update(x=3, y=5)
            Object(x=3, y=5, z=0)

            >>> obj = Object(x=0, y=Object(x=0, y=2, z=0), z=0)
            >>> obj.update(x=2, y__x=5)
            Object(x=2, y=Object(x=5, y=2, z=0), z=0)
        """
        assert is_dataclass(self), "only works on dataclasses."

        top_attrs = {k: v for k, v in kwargs.items() if not '__' in k}
        deep_attrs = {k: v for k, v in kwargs.items() if '__' in k}
        for key, value in deep_attrs.items():
            attr, nextattr = key.split('__')
            val = replace(getattr(self, attr), **{nextattr: value})
            top_attrs[attr] = val

        return replace(self, **top_attrs)
