import os.path

from krcg import twda
from krcg import vtes


def pytest_sessionstart(session):
    """Do not launch tests is there is no proper Internet connection.

    This is not very graceful
    """
    vtes.VTES.load_from_vekn()
    """Use to initialize the twda to the 20 decks test snapshot."""
    with open(os.path.join(os.path.dirname(__file__), "twda_test.html")) as f:
        twda.TWDA.load_html(f)
