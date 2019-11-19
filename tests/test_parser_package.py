import re
from unittest import mock

import pytest

from avwx.parsers import RegexAtom, AtomSpan, AtomHandler, CanNotHandleError


@pytest.fixture
def pattern_string():
    return r"\bSOME PATTERN P(?P<digits>\d{1,5})\b"


@pytest.fixture
def pattern(pattern_string):
    return re.compile(pattern_string)


@pytest.fixture
def regex_atom(pattern):
    return RegexAtom(pattern, name="Some Pattern")


@pytest.fixture
def some_pattern_handler(regex_atom) -> AtomHandler:
    def translate_some_pattern(match: re.Match) -> str:
        digits = match.groupdict()["digits"]
        return f"Some Translated Data: {digits}"

    handler = AtomHandler(regex_atom, translate_some_pattern)

    return handler


SUCCESS_STRING = "HERE IS SOME PATTERN P123 THING"
FAIL_STRING = "YOU HAVE NO MATCH HERE"


class TestRegexAtom:
    def test_constructor(self, regex_atom, pattern):
        atom = regex_atom
        assert atom is not None
        assert atom.regex == pattern
        assert isinstance(atom._regex, re.Pattern)
        assert atom.name == "Some Pattern"

    def test_to_atom_span(self, regex_atom):
        exp = AtomSpan(match="SOME PATTERN P123", start=8, end=25)
        match, start, end = regex_atom.to_atom_span(SUCCESS_STRING)

        assert regex_atom.to_atom_span(SUCCESS_STRING) == exp
        assert SUCCESS_STRING[start:end] == match

    def test_is_in(self, regex_atom):
        assert regex_atom.is_in(SUCCESS_STRING)

    def test_from_pattern_string(self, pattern_string):
        atom = RegexAtom.from_pattern_string(pattern_string, name="some pattern")

        assert atom.is_in(SUCCESS_STRING)
        assert not atom.is_in(FAIL_STRING)

    def test_from_pattern_string_with_flag(self, pattern_string):
        string_parts = pattern_string.split()
        string_parts[0] = string_parts[0].lower()

        lower_string = " ".join(string_parts)

        atom = RegexAtom.from_pattern_string(lower_string, re.I, re.M)

        assert atom.is_in(SUCCESS_STRING)
        assert not atom.is_in(FAIL_STRING)


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
