import abc
from typing import Dict, Union, Optional, TYPE_CHECKING, Callable

from .exceptions import CanNotHandleError, TranslationError

if TYPE_CHECKING:
    from .atom import RegexAtom
    from re import Match


class RegexAtomHandler:
    """Handle the individual translation of an atom"""

    def __init__(
        self, atom: "RegexAtom", translation_callable: Callable[["Match"], str]
    ):
        self.atom = atom
        self.translation_callable = translation_callable

    def __repr__(self):
        return f"{type(self).__name__}(atom={self.atom!r})"

    def __call__(self, *args, **kwargs):
        return self.translate_atom(*args, **kwargs)

    @property
    def translation_callable(self):
        return self._translation_callable

    @translation_callable.setter
    def translation_callable(self, new_callable: Callable[["Match"], str]):
        if not callable(new_callable):
            raise TypeError("translation_callable must be a callable")
        self._translation_callable = new_callable

    def can_handle(self, atom_string: str) -> bool:
        """Return True if handler is qualified to handle translation"""
        return self.atom.is_in(atom_string)

    # fixme: atom_string or entire string
    # todo: allow for default error handling option
    def translate_atom(self, atom_string: str) -> str:
        """Perform translation on the atom string"""
        match = self.atom.search(atom_string)
        if not match:
            raise CanNotHandleError(
                f"{self.atom!r} has nothing to translate from {atom_string!r}"
            )
        result = self.translation_callable(match)

        return result
