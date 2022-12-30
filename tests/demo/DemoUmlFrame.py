
from logging import Logger
from logging import getLogger

from wx import Window

from miniogl.DiagramFrame import DiagramFrame
from ogl.events.IOglEventEngine import IEventEngine

DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20


class DemoUmlFrame(DiagramFrame):
    def __init__(self, parent: Window, eventEngine: IEventEngine):

        self.logger:          Logger       = getLogger(__name__)
        self._oglEventEngine: IEventEngine = eventEngine

        super().__init__(parent=parent)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

    @property
    def eventEngine(self) -> IEventEngine:
        return self._oglEventEngine
