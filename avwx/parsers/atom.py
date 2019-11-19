import abc
import re
from typing import Optional, Any, NamedTuple, Union, Tuple, Iterable


class AtomSpan(NamedTuple):
    """
    Finding within a string. Can be used for slicing as `end` is non-inclusive.
    """

    match: Optional[str]
    start: Optional[int]
    end: Optional[int]


class BaseAtom(abc.ABC):
    """Atom represents a single encoded entity in an encoded string"""

    @abc.abstractmethod
    def search(self, item: str) -> AtomSpan:
        """Return a StringSpan. If no match found, return a StringSpan(None, None, None)"""
        pass

    def is_in(self, string) -> bool:
        """Return True if the Atom is in the string"""
        return self.search(string).match is not None


class RegexAtom(BaseAtom):
    """Atom defined by regex pattern"""

    def __init__(self, regex_pattern: re.Pattern, name: Optional[str] = None):
        self.regex = regex_pattern
        self.name = name

    def __repr__(self):
        return f"{type(self).__name__}(pattern={self.regex!r}, name={self.name})"

    @property
    def regex(self) -> re.Pattern:
        return self._regex

    @regex.setter
    def regex(self, regex: re.Pattern):
        if not isinstance(regex, re.Pattern):
            raise TypeError("regex must be a compiled `re.Pattern`")
        self._regex = regex

    @classmethod
    def from_pattern_string(
        cls, pattern: str, *flags: re.RegexFlag, name: Optional[str] = None
    ) -> "RegexAtom":
        """
        Return a new instance of `RegexAtom` from a string pattern.

        :param pattern: string to be compiled into regex pattern
        :param flags: flags to pass to `re.compile`
        :param name: name for repr
        """

        if flags:
            regex = re.compile(pattern, sum(flags))
        else:
            regex = re.compile(pattern)

        out = cls(regex, name=name)

        return out

    def search(self, string: str) -> AtomSpan:
        """
        Search the string for the atom
        """
        match = self.regex.search(string)
        if match:
            start, stop = match.span()
            return AtomSpan(match=match.group(), start=start, end=stop)
        return AtomSpan(None, None, None)
