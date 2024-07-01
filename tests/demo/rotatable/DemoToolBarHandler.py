
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
from tests.demo.rotatable.RotatableArc import RotatableArc
from tests.demo.rotatable.RotatableCircle import RotatableCircle
from tests.demo.rotatable.RotatableEllipse import RotatableEllipse
from tests.demo.rotatable.RotatableEllipticArc import RotatableEllipticArc
from tests.demo.rotatable.RotatablePolygon import RotatablePolygon
from tests.demo.rotatable.RotatableRectangle import RotatableRectangle
from tests.demo.rotatable.icons.rectangle64 import embeddedImage as ImgRectangle
from tests.demo.rotatable.icons.redCircle32 import embeddedImage as ImgCircle
from tests.demo.rotatable.icons.ellipse32 import embeddedImage as ImgEllipse
from tests.demo.rotatable.icons.polygon64 import embeddedImage as ImgPolygon
from tests.demo.rotatable.icons.arc32 import embeddedImage as ImgArc
from tests.demo.rotatable.icons.ellipticalArc64 import embeddedImage as ImgEllipticalArc
from tests.demo.rotatable.icons.line32 import embeddedImage as ImgLine
from tests.demo.rotatable.icons.rotateClockwise64 import embeddedImage as ImgRotateClockwise
from tests.demo.rotatable.icons.rotateCounterClockwise64 import embeddedImage as ImgRotateCounterClockwise
from tests.demo.rotatable.icons.clear64 import embeddedImage as ImgClear


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

NO_ROTATABLE_SHAPE = cast(RotatableShape, None)


class DemoToolBarHandler:
    def __init__(self, frame: SizedFrame, diagramFrame: DemoRotatableShapeFrame):

        self.logger: Logger = getLogger(__name__)

        self._tb:           ToolBar    = frame.CreateToolBar(TB_HORIZONTAL | TB_TEXT | TB_RIGHT)
        self._frame:        SizedFrame = frame
        self._diagramFrame: DemoRotatableShapeFrame = diagramFrame

        self._ID_CLEAR:                    WindowIDRef = wxNewIdRef()
        self._ID_DISPLAY_POLYGON:                  WindowIDRef = wxNewIdRef()
        self._ID_DISPLAY_RECTANGLE:        WindowIDRef = wxNewIdRef()
        self._ID_DISPLAY_CIRCLE:           WindowIDRef = wxNewIdRef()
        self._ID_DISPLAY_ELLIPSE:          WindowIDRef = wxNewIdRef()
        self._ID_DISPLAY_ARC:              WindowIDRef = wxNewIdRef()
        self._ID_DISPLAY_ELLIPTICAL_ARC:   WindowIDRef = wxNewIdRef()
        self._ID_ROTATE_CLOCKWISE:         WindowIDRef = wxNewIdRef()
        self._ID_ROTATE_COUNTER_CLOCKWISE: WindowIDRef = wxNewIdRef()

        self._x: int = 200
        self._y: int = 200

        self._rotatableShape: RotatableShape = NO_ROTATABLE_SHAPE

        self._tb.SetToolBitmapSize(Size(24, 24))

        for td in self._toolBarDefintions():
            tDef: ToolBarDefinition = cast(ToolBarDefinition, td)
            self._tb.AddTool(tDef.toolId, tDef.label, tDef.bitMap, tDef.shortHelp, tDef.itemKind)

        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_CLEAR)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_RECTANGLE)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_CIRCLE)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_ELLIPSE)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_ARC)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_POLYGON)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_DISPLAY_ELLIPTICAL_ARC)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_ROTATE_CLOCKWISE)
        self._frame.Bind(EVT_TOOL, self._onDisplayElement, id=self._ID_ROTATE_COUNTER_CLOCKWISE)

    @property
    def toolbar(self) -> ToolBar:
        return self._tb

    def _toolBarDefintions(self) -> ToolBarDefinitions:

        toolBarDefinitions: ToolBarDefinitions = ToolBarDefinitions(
            [
                ToolBarDefinition(label='Clear',     bitMap=ImgClear.Bitmap,     toolId=self._ID_CLEAR,             itemKind=ITEM_NORMAL, shortHelp='Clear'),
                ToolBarDefinition(label='Rectangle', bitMap=ImgRectangle.Bitmap, toolId=self._ID_DISPLAY_RECTANGLE, itemKind=ITEM_NORMAL, shortHelp='Rectangle'),
                ToolBarDefinition(label='Circle',    bitMap=ImgCircle.Bitmap,    toolId=self._ID_DISPLAY_CIRCLE,    itemKind=ITEM_NORMAL, shortHelp='Circle'),
                ToolBarDefinition(label='Ellipse',   bitMap=ImgEllipse.Bitmap,   toolId=self._ID_DISPLAY_ELLIPSE,   itemKind=ITEM_NORMAL, shortHelp='Ellipse'),
                ToolBarDefinition(label='Arc',       bitMap=ImgArc.Bitmap,       toolId=self._ID_DISPLAY_ARC,       itemKind=ITEM_NORMAL, shortHelp='Arc'),
                ToolBarDefinition(label='Polygon', bitMap=ImgPolygon.Bitmap,     toolId=self._ID_DISPLAY_POLYGON,   itemKind=ITEM_NORMAL, shortHelp='Polygon'),

                ToolBarDefinition(label='Line', bitMap=ImgLine.Bitmap, toolId=wxNewIdRef(), itemKind=ITEM_NORMAL, shortHelp='Line'),

                ToolBarDefinition(label='Elliptical Arc',   bitMap=ImgEllipticalArc.Bitmap,          toolId=self._ID_DISPLAY_ELLIPTICAL_ARC,
                                  itemKind=ITEM_NORMAL, shortHelp='Elliptical Arc'),
                ToolBarDefinition(label='ClockWise',        bitMap=ImgRotateClockwise.Bitmap,        toolId=self._ID_ROTATE_CLOCKWISE,
                                  itemKind=ITEM_NORMAL, shortHelp='Rotate Clockwise'),
                ToolBarDefinition(label='CounterClockWise', bitMap=ImgRotateCounterClockwise.Bitmap, toolId=self._ID_ROTATE_COUNTER_CLOCKWISE,
                                  itemKind=ITEM_NORMAL, shortHelp='Rotate CounterClockwise'),
            ]
        )

        return toolBarDefinitions

    def _onDisplayElement(self, event: CommandEvent):
        toolId: int = event.GetId()
        match toolId:
            case self._ID_CLEAR:
                self._clear()
            case self._ID_DISPLAY_RECTANGLE:
                self._displayRectangle()
            case self._ID_DISPLAY_CIRCLE:
                self._displayCircle()
            case self._ID_DISPLAY_ELLIPSE:
                self._displayEllipse()
            case self._ID_DISPLAY_ARC:
                self._displayArc()
            case self._ID_DISPLAY_POLYGON:
                self._displayPolygon()
            case self._ID_DISPLAY_ELLIPTICAL_ARC:
                self._displayEllipticalArc()
            case self._ID_ROTATE_CLOCKWISE:
                self._rotateShape(clockWise=True)
            case self._ID_ROTATE_COUNTER_CLOCKWISE:
                self._rotateShape(clockWise=False)
            case _:
                self.logger.error(f'WTH!  I am not handling that menu item {toolId=}')

    def _clear(self):
        diagram = self._diagramFrame.diagram
        diagram.RemoveShape(self._rotatableShape)
        self._diagramFrame.Refresh()
        self._rotatableShape = NO_ROTATABLE_SHAPE

    def _displayRectangle(self):

        rotatableShape: RotatableRectangle = RotatableRectangle()

        rotatableShape.draggable = True

        self._rotatableShape = rotatableShape

        self._addToDiagram(rotatableShape=rotatableShape)

    def _displayCircle(self):

        rotatableShape: RotatableCircle = RotatableCircle()
        rotatableShape.draggable = True

        self._rotatableShape = rotatableShape

        self._addToDiagram(rotatableShape=rotatableShape)

    def _displayEllipse(self):
        rotatableShape: RotatableEllipse = RotatableEllipse()
        rotatableShape.draggable = True

        self._rotatableShape = rotatableShape

        self._addToDiagram(rotatableShape=rotatableShape)

    def _displayArc(self):
        self._finishDisplay(RotatableArc())

    def _displayPolygon(self):
        self._finishDisplay(RotatablePolygon())

    def _displayEllipticalArc(self):
        self._finishDisplay(RotatableEllipticArc())

    def _rotateShape(self, clockWise: bool):
        self._rotatableShape.Rotate(clockwise=clockWise)
        self._diagramFrame.Refresh()

    def _finishDisplay(self, rotatableShape: RotatableShape):
        rotatableShape.draggable = True

        self._rotatableShape = rotatableShape

        self._addToDiagram(rotatableShape=rotatableShape)

    def _addToDiagram(self, rotatableShape: RotatableShape):

        x, y = self._getPosition()
        rotatableShape.SetPosition(x, y)
        self._diagramFrame.Refresh()

        diagram = self._diagramFrame.diagram
        diagram.AddShape(rotatableShape, withModelUpdate=True)

        self.logger.info(f'{diagram.shapes=}')

    def _getPosition(self) -> Tuple[int, int]:
        x: int = self._x
        y: int = self._y

        # self._x += INCREMENT_X
        # self._y += INCREMENT_Y
        return x, y
