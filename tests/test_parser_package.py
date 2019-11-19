import re

import pytest

from avwx.parsers import RegexAtom, AtomSpan


@pytest.fixture
def pattern_string():
    return r"\bSOME PATTERN P(?P<digits>\d{1,5})\b"


@pytest.fixture
def pattern(pattern_string):
    return re.compile(pattern_string)


@pytest.fixture
def regex_atom(pattern):
    return RegexAtom(pattern, name="Some Pattern")


SUCCESS_STRING = "HERE IS SOME PATTERN P123 THING"
FAIL_STRING = "YOU HAVE NO MATCH HERE"


class TestRegexAtom:
    def test_constructor(self, regex_atom, pattern):
        atom = regex_atom
        assert atom is not None
        assert atom.regex == pattern
        assert isinstance(atom._regex, re.Pattern)
        assert atom.name == "Some Pattern"

    def test_search(self, regex_atom):
        exp = AtomSpan(match="SOME PATTERN P123", start=8, end=25)
        match, start, end = regex_atom.search(SUCCESS_STRING)

        assert regex_atom.search(SUCCESS_STRING) == exp
        assert SUCCESS_STRING[start:end] == match

    def test_contains(self, regex_atom):
        assert regex_atom.is_in(SUCCESS_STRING)

    def test_from_pattern(self, pattern_string):
        atom = RegexAtom.from_pattern_string(pattern_string, name="some pattern")

        assert atom.is_in(SUCCESS_STRING)
        assert not atom.is_in(FAIL_STRING)

    def test_from_pattern_with_flag(self, pattern_string):
        string_parts = pattern_string.split()
        string_parts[0] = string_parts[0].lower()

        lower_string = " ".join(string_parts)

        atom = RegexAtom.from_pattern_string(lower_string, re.I, re.M)

        assert atom.is_in(SUCCESS_STRING)
        assert not atom.is_in(FAIL_STRING)
