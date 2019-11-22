"""
Package containing parsing feature
"""
from typing import Dict, List, Iterator, Set

from .atom import BaseAtom, RegexAtom, AtomSpan
from .atom_handlers import AtomHandler
from .exceptions import CanNotHandleError, TranslationError


class Parser:
    def __init__(self):
        self._handlers: List[AtomHandler] = []

    @property
    def handlers(self):
        return list(self._handlers)

    def register_handler(self, handler: AtomHandler) -> None:
        """Register a handler"""
        if not isinstance(handler, AtomHandler):
            raise TypeError(f"handler must be of type {type(AtomHandler.__name__)}")
        self._handlers.append(handler)

    def unregister_handler(self, handler: AtomHandler) -> AtomHandler:
        """Unregister a handler"""
        try:
            idx = self._handlers.index(handler)
            return self._handlers.pop(idx)
        except IndexError:
            raise IndexError(f"{handler} not registered to parser")

    """
    Preconditions:
        - String
        
    Input:
        - String that may contain Atoms
        
    Output:
        - Dict:
            - keys: extracted raw matches from input string
            - values: result of translate call on handler
        
    STEPS:
    ------
    make a dict to accept translations
    get all of the handlers that can perform translations on the string
    get the first applicable handler
    while there is a good handler
        if the handler can still perform translation
            perform the translation
            if an error occurs during translation
                OPTION 1: add raw: Error Message to translation
                    - `prepend_error = str`
                OPTION 2: raise to caller and abort
                    - if `strict` set to True
            extract the raw text from the string
            add the translation to the results dict with the raw string
    return the dict
    """

    def parse_into_translations(
        self, string: str, strict: bool = True, prepend_error: str = "ERROR: "
    ) -> Dict[str, str]:
        """Parse a string into a dict of raw:translated string value pairs"""
        if not isinstance(string, str):
            raise TypeError("'string' must be a str")
        if not string:
            return {}

        out: Dict[str, str] = {}

        working_string = string[::]
        valid_handlers = self._iter_handlers_that_can_handle_string(working_string)
        current_handler = next(valid_handlers)

        failed_handlers: Set[AtomHandler] = set()

        while current_handler is not None:
            try:
                if current_handler in failed_handlers:
                    current_handler = next(valid_handlers)
                    continue

                translation = current_handler.translate(working_string)
                raw, working_string = current_handler.atom.extract_atom_from_string(
                    working_string
                )

                out[raw] = translation
                current_handler = next(valid_handlers)

            except TranslationError as e:
                if strict is False:
                    error_str = str(e)
                    translation = prepend_error + error_str
                    out[current_handler.atom.name] = translation
                    failed_handlers.add(current_handler)
                else:
                    raise e
            except StopIteration:
                break

        return out

    def _iter_handlers_that_can_handle_string(
        self, string: str
    ) -> Iterator[AtomHandler]:
        return (handler for handler in self.handlers if handler.can_handle(string))
