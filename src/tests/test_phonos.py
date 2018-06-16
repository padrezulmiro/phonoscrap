import pytest
from collections import namedtuple
from src.scrapper.phonos import Phonos


OrthoSyl = namedtuple('OrthoSyl', ['ortho', 'strongaccent', 'weakaccent', 'previous'])
words = [
    {
        'ortho': [
            OrthoSyl('hi', False, False, False),
            OrthoSyl('a', True, True, False),
            OrthoSyl('to', False, False, False)
        ],
        'phono': ["i", "ˈa", "tu"]
    },

    {
        'ortho': [
            OrthoSyl('á', False, True, False),
            OrthoSyl('bê', False, True, False),
            OrthoSyl('cê', True, True, False)
        ],
        'phono': [',a','bˌe','sˈe']
    }
]


@pytest.fixture(params=words)
def phonos(request):
    return Phonos(request.ortho, request.phono)


def test_ortho_word(phonos):
    assert phonos.ortho_word == "hiato"


def test_phono_word(phonos):
    assert phonos.phono_word() == "i'atu"


def test_ortho_strong_accent(phonos):
    assert phonos


def test_phono_strong_accent():
    pass


def test_weak_accents():
    pass