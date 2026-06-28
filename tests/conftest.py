import pytest

from krcg import loader
from krcg import twda


@pytest.fixture(scope="session")
def cards():
    """The cards library, built offline from the packaged krcg snapshot."""
    return loader.load_local()


@pytest.fixture(scope="session")
def TWDA():
    """The TWDA, built offline from the packaged krcg snapshot."""
    return twda.load_local()
