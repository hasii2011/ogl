
from typing import Callable

from logging import Logger
from logging import getLogger

from enum import Enum

from wx import PostEvent
from wx import PyEventBinder
from wx import Window

from wx.lib.newevent import NewEvent


SetStatusTextEvent,  EVT_SET_STATUS_TEXT   = NewEvent()


class DemoEventType(Enum):
    SET_STATUS_TEXT = 'SetStatusText'


class DemoEventEngine:
    def __init__(self, listeningWindow: Window):

        self._listeningWindow: Window = listeningWindow
        self.logger:           Logger = getLogger(__name__)

    def registerListener(self, event: PyEventBinder, callback: Callable):
        self._listeningWindow.Bind(event, callback)

    def sendEvent(self, eventType: DemoEventType, **kwargs):
        """
        Args:
            eventType:
            **kwargs:
        """
        match eventType:
            case DemoEventType.SET_STATUS_TEXT:
                self._sendSetStatusTextEvent(**kwargs)
            case _:
                self.logger.warning(f'Unknown Demo Event Type: {eventType}')

    def _sendSetStatusTextEvent(self, **kwargs):

        statusMessage: str = kwargs['statusMessage']
        eventToPost: SetStatusTextEvent = SetStatusTextEvent(statusMessage=statusMessage)  # type: ignore
        PostEvent(dest=self._listeningWindow, event=eventToPost)
