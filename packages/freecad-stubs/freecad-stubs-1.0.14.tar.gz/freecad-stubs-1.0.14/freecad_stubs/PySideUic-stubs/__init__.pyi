import typing


# UiLoader.cpp
def loadUiType() -> tuple[typing.Any, typing.Any] | None:
    """
    PySide lacks the "loadUiType" command, so we have to convert the ui file to py code in-memory first
    and then execute it in a special frame to retrieve the form_class.
    Possible exceptions: (Exception).
    """


def loadUi() -> typing.Any | None:
    """
    Addition of "loadUi" to PySide.
    Possible exceptions: (Exception).
    """


def createCustomWidget():
    """Create custom widgets."""
