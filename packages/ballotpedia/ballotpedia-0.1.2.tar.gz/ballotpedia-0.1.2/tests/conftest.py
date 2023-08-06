"""conftest.py for ballotpedia."""
import pytest

from ballotpedia.api import Ballotpedia


@pytest.fixture
def fixture_ballotpedia():
    return Ballotpedia("FAKEAPI")
