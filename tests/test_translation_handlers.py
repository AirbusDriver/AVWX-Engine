import pytest
from unittest import mock

from avwx.parsing.atom_handlers import AtomHandler, BaseAtom
from avwx.parsing.exceptions import CanNotHandleError

SAMPLE_STRING = "THIS IS A SAMPLE STRING WITH 3NC0D3D DATA"


def translate_sample_string(atom: BaseAtom, string: str) -> str:
    return "Decoded: 303"


@pytest.fixture
def mocked_atom_handler() -> AtomHandler:
    """
    AtomHandler with a mocked atom that can be configured before
    handler test calls. The translation callable simply returns
    "Decoded: 303" and should be mocked for different behaviors.

    Default mocked calls:
        * atom.name = "Sample Atom"
    """
    mock_atom = mock.MagicMock()
    mock_atom.name = "Sample Atom"

    handler = AtomHandler(mock_atom, translate_sample_string)

    return handler


class TestAtomHandler:
    def test_can_handle(self, mocked_atom_handler):
        handler = mocked_atom_handler
        handler.atom.is_in.return_value = True

        assert handler.can_handle(SAMPLE_STRING)

        handler.atom.is_in.return_value = False

        assert not handler.can_handle(SAMPLE_STRING)

    def test_translate_atom(self, mocked_atom_handler):
        handler = mocked_atom_handler
        handler.atom.is_in.return_value = True

        result = handler.translate(SAMPLE_STRING)

        assert result == "Decoded: 303" == handler(SAMPLE_STRING)

    def test_translate_atom_raises_for_can_not_handle(self, mocked_atom_handler):
        handler = mocked_atom_handler
        handler.atom.is_in.return_value = False

        with pytest.raises(CanNotHandleError) as exc_info:
            result = handler.translate(SAMPLE_STRING)

        expected = f"{handler.atom!r} has nothing to translate from {SAMPLE_STRING!r}"

        assert expected in str(exc_info.value)
