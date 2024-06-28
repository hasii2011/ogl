
from typing import List
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import Bitmap
from wx import CommandEvent
from wx import EVT_TOOL
from wx import ITEM_NORMAL
from wx import Size
from wx import TB_HORIZONTAL
from wx import TB_RIGHT
from wx import TB_TEXT
from wx import ToolBar
from wx import WindowIDRef

from wx import NewIdRef as wxNewIdRef
from wx.lib.sized_controls import SizedFrame

from miniogl.rotatable.RotatableShape import RotatableShape
from tests.demo.rotatable.DemoRotatableShapeFrame import DemoRotatableShapeFrame
from tests.demo.rotatable.RotatableRectangle import RotatableRectangle
from tests.demo.rotatable.icons.rectangle64 import embeddedImage as ImgRectangle
from tests.demo.rotatable.icons.redCircle32 import embeddedImage as ImgCircle
from tests.demo.rotatable.icons.ellipse32 import embeddedImage as ImgEllipse
from tests.demo.rotatable.icons.polygon64 import embeddedImage as ImgPolygon
from tests.demo.rotatable.icons.arc32 import embeddedImage as ImgArc
from tests.demo.rotatable.icons.line32 import embeddedImage as ImgLine


@dataclass
class ToolBarDefinition:
    label:     str
    bitMap:    Bitmap
    toolId:    WindowIDRef
    itemKind:  int
    shortHelp: str


ToolBarDefinitions = NewType('ToolBarDefinitions', List[ToolBarDefinition])

INITIAL_X:   int = 100
INITIAL_Y:   int = 100

INCREMENT_X: int = INITIAL_X + 20
INCREMENT_Y: int = INITIAL_Y + 100


class DemoToolBarHandler:
    def __init__(self, frame: SizedFrame, diagramFrame: DemoRotatableShapeFrame):

        self.logger: Logger = getLogger(__name__)

        self._tb:           ToolBar    = frame.CreateToolBar(TB_HORIZONTAL | TB_TEXT | TB_RIGHT)
        self._frame:        SizedFrame = frame
        self._diagramFrame: DemoRotatableShapeFrame = diagramFrame

        self._ID_DISPLAY_RECTANGLE: WindowIDRef = wxNewIdRef()
        self._ID_ROTATE_RECTANGLE:  WindowIDRef = wxNewIdRef()

        self._x: int = 200
        self._y: int = 200

        self._tb.SetToolBitmapSize(Size(24, 24))

        for td in self._toolBarDefintions():
            tDef: ToolBarDefinition = cast(ToolBarDefinition, td)
            self._tb.AddTool(tDef.toolId, tDef.label, tDef.bitMap, tDef.shortHelp, tDef.itemKind)

        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_RECTANGLE)

    @property
    def toolbar(self) -> ToolBar:
        return self._tb

    def _toolBarDefintions(self) -> ToolBarDefinitions:

        toolBarDefinitions: ToolBarDefinitions = ToolBarDefinitions(
            [
                ToolBarDefinition(label='Rectangle', bitMap=ImgRectangle.Bitmap, toolId=self._ID_DISPLAY_RECTANGLE, itemKind=ITEM_NORMAL, shortHelp='Rectangle'),
                ToolBarDefinition(label='Circle',    bitMap=ImgCircle.Bitmap,    toolId=wxNewIdRef(), itemKind=ITEM_NORMAL, shortHelp='Circle'),
                ToolBarDefinition(label='Ellipse',   bitMap=ImgEllipse.Bitmap,   toolId=wxNewIdRef(), itemKind=ITEM_NORMAL, shortHelp='Ellipse'),
                ToolBarDefinition(label='Polygon',   bitMap=ImgPolygon.Bitmap,   toolId=wxNewIdRef(), itemKind=ITEM_NORMAL, shortHelp='Polygon'),
                ToolBarDefinition(label='Arc',       bitMap=ImgArc.Bitmap,       toolId=wxNewIdRef(), itemKind=ITEM_NORMAL, shortHelp='Arc'),
                ToolBarDefinition(label='Line',      bitMap=ImgLine.Bitmap,      toolId=wxNewIdRef(), itemKind=ITEM_NORMAL, shortHelp='Line'),
            ]
        )

        return toolBarDefinitions

    def _onDisplayElement(self, event: CommandEvent):
        toolId: int = event.GetId()
        match toolId:
            case self._ID_DISPLAY_RECTANGLE:
                self._displayRectangle()
            case _:
                self.logger.error(f'WTH!  I am not handling that menu item')

    def _displayRectangle(self):

        rotatableShape: RotatableRectangle = RotatableRectangle()

        rotatableShape.draggable = True

        self._addToDiagram(rotatableShape=rotatableShape)

    def _addToDiagram(self, rotatableShape: RotatableShape):

        x, y = self._getPosition()
        rotatableShape.SetPosition(x, y)
        self._diagramFrame.Refresh()

        diagram = self._diagramFrame.diagram
        diagram.AddShape(rotatableShape, withModelUpdate=True)

        self.logger.info(f'{diagram.GetShapes()=}')

    def _getPosition(self) -> Tuple[int, int]:
        x: int = self._x
        y: int = self._y

        self._x += INCREMENT_X
        self._y += INCREMENT_Y
        return x, y
