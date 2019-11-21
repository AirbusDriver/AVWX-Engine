import re
from unittest import mock

import pytest

from avwx.parsers import RegexAtom, AtomSpan, AtomHandler, CanNotHandleError


@pytest.fixture
def some_pattern_handler(regex_atom) -> AtomHandler:
    def translate_some_pattern(match: re.Match) -> str:
        digits = match.groupdict()["digits"]
        return f"Some Translated Data: {digits}"

    handler = AtomHandler(regex_atom, translate_some_pattern)

    return handler


SUCCESS_STRING = "HERE IS SOME PATTERN P123 THING"
FAIL_STRING = "YOU HAVE NO MATCH HERE"


class TestAtomHandler:
    def test_instance(self, some_pattern_handler, regex_atom):
        handler = some_pattern_handler

        assert handler is not None
        assert repr(regex_atom) in repr(handler)

    def test_translate(self, some_pattern_handler):
        handler = some_pattern_handler

        expected = "Some Translated Data: 123"

        assert handler.translate_atom(SUCCESS_STRING) == expected

    def test_call(self, some_pattern_handler):
        handler = some_pattern_handler

        assert handler(SUCCESS_STRING) == handler.translate_atom(SUCCESS_STRING)

    def test_translate_raises(self, some_pattern_handler):
        handler = some_pattern_handler
        handler.atom.search = mock.MagicMock(return_value=None)

        with pytest.raises(CanNotHandleError):
            handler.translate_atom(SUCCESS_STRING)

    @pytest.mark.xfail(reason="not implemented")
    def test_translation_error_raised(self, some_pattern_handler):
        assert 0
