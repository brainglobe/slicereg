from __future__ import annotations

import inspect
from typing import Type, TypeVar

T = TypeVar('T')


class DependencyInjector:
    """Simple Dependency Injection class."""

    def __init__(self, **kwargs):
        self.attrs = kwargs

    def inject(self, command: Type[T]) -> T:
        """
        Constructs a command, mapping Commandbuilder's inputs to its inputs.

        Example:
        >> CommandBuilder(_repo=ImageRepo).build(LoadSection)
        LoadSection(_repo=ImageRepo)
        """

        args = tuple(inspect.signature(command).parameters)
        kwargs = {arg: self.attrs[arg] for arg in args}
        return command(**kwargs)  # type: ignore
