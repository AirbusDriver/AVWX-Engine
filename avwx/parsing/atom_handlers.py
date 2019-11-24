"""
RegexAtomHandler:
    * bundles atom and some translation callable together to be executed with arbitrary strings
    * translation callables are bound to the atom handler by decorator naming the atom

TranslationCallable:
    * A client defined callable that operates on an Atom and an input string

    example:


        def sea_level_pressure_translation(SLP_ATOM, input_: str) -> str:
            match = SLP_ATOM.to_atom_span(input_).match
            if not match:
                raise TranslationError("some descriptive error")
            else:
                pressure = match[3:].strip()

            return f"Sea Level Pressure {pressure}"

        -- or with a RegEx Atom --

        def sea_level_pressure_translation(SLP_ATOM: RegexAtom, input_: str) -> str:
            match = SLP_ATOM.search(input_)
            if not match:
                raise TranslationError("some descriptive error")
            else:
                data = match.groupdict()

            return f"Sea Level Pressure {data["pressure"]}"

    * TranslationError - should be raised when there is a problem during the translation.
        - This should be used instead of a ValueError so that the handler can decide what to do instead. Maybe
        a default translation or error code should be used instead for cleanup
"""

import abc
from typing import Dict, Union, Optional, TYPE_CHECKING, Callable, Any
import re

from .exceptions import CanNotHandleError, TranslationError
from .atom import BaseAtom


# todo: multiple translations for a single atom
class AtomHandler:
    """Handle the individual translation of an atom"""

    def __init__(
        self, atom: BaseAtom, translation_callable: Callable[[BaseAtom, str], str]
    ):
        self.atom = atom
        self.translation_callable = translation_callable

    def __repr__(self):
        return f"{type(self).__name__}(atom: {self.atom.name})"

    def __call__(self, *args, **kwargs):
        return self.translate(*args, **kwargs)

    @property
    def translation_callable(self):
        return self._translation_callable

    @translation_callable.setter
    def translation_callable(self, new_callable: Callable[[BaseAtom, str], str]):
        if not callable(new_callable):
            raise TypeError(
                "translation_callable must be a callable that accepts a `BaseAtom` and a string"
            )
        self._translation_callable = new_callable

    def can_handle(self, atom_string: str) -> bool:
        """Return True if handler is qualified to handle translation"""
        return self.atom.is_in(atom_string)

    # todo: allow for default error handling option
    def translate(self, string: str) -> str:
        """Perform translation on the atom string"""
        if not self.atom.is_in(string):
            raise CanNotHandleError(
                f"{self.atom!r} has nothing to translate from {string!r}"
            )
        result = self.translation_callable(self.atom, string)

        return result
