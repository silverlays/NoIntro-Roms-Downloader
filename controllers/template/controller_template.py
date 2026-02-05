from typing import TypeVar, Generic

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QWidget

T = TypeVar("T", bound=QWidget)


class ControllerTemplate(QObject, Generic[T]):
    InvoquePreviousView = Signal()
    InvoqueNextView = Signal()

    def __init__(self, view: T):
        super().__init__()
        self._view: T = view

    @property
    def View(self):
        return self._view
