
from logging import Logger
from logging import getLogger

from wx import Window

from miniogl.DiagramFrame import DiagramFrame
from ogl.events.IOglEventEngine import IEventEngine


class DemoUmlFrame(DiagramFrame):
    def __init__(self, parent: Window, eventEngine: IEventEngine):

        self.logger:          Logger       = getLogger(__name__)
        self._oglEventEngine: IEventEngine = eventEngine

        super().__init__(parent=parent)

    @property
    def eventEngine(self) -> IEventEngine:
        return self._oglEventEngine
