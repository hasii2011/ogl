
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import App
from wx import Bitmap
from wx import BitmapBundle
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import FRAME_FLOAT_ON_PARENT
from wx import FRAME_TOOL_WINDOW
from wx import ID_EXIT
from wx import ITEM_NORMAL
from wx import Menu
from wx import MenuBar
from wx import NO_BORDER

from wx import NewIdRef as wxNewIdRef
from wx import NullBitmap
from wx import TB_FLAT
from wx import WindowIDRef
from wx import ToolBar

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from miniogl.Diagram import Diagram
from miniogl.rotatable.RotatableShape import RotatableShape

from tests.ProjectTestBase import ProjectTestBase

from tests.demo.rotatable.DemoRotatableShapeFrame import DemoRotatableShapeFrame
from tests.demo.rotatable.RotatableRectangle import RotatableRectangle

FRAME_WIDTH:  int = 800
FRAME_HEIGHT: int = 600

INITIAL_X:   int = 100
INITIAL_Y:   int = 100

INCREMENT_X: int = INITIAL_X + 20
INCREMENT_Y: int = INITIAL_Y + 100


class DemoRotatableShapes(App):
    def __init__(self):

        ProjectTestBase.setUpLogging()

        self.logger: Logger = getLogger(__name__)

        self._frame:          SizedFrame            = cast(SizedFrame, None)
        self._diagramFrame:   DemoRotatableShapeFrame = cast(DemoRotatableShapeFrame, None)
        self._diagram:        Diagram               = cast(Diagram, None)

        self._ID_DISPLAY_RECTANGLE: int = wxNewIdRef()
        self._ID_ROTATE_RECTANGLE:  int = wxNewIdRef()

        self._x: int = 200
        self._y: int = 200

        self._rotatableShape: RotatableRectangle = cast(RotatableRectangle, None)

        super().__init__(redirect=False)

    def OnInit(self):

        frameStyle: int = DEFAULT_FRAME_STYLE | FRAME_FLOAT_ON_PARENT | FRAME_TOOL_WINDOW

        self._frame = SizedFrame(parent=None, title="Test Rotatable Shapes", size=(FRAME_WIDTH, FRAME_HEIGHT), style=frameStyle)
        self._frame.CreateStatusBar()  # should always do this when there's a resize border

        sizedPanel: SizedPanel = self._frame.GetContentsPane()

        self._diagramFrame = DemoRotatableShapeFrame(parent=sizedPanel)
        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)

        # Some incestuous behavior going on here
        self._diagram = Diagram(panel=self._diagramFrame)
        self._diagramFrame.diagram = self._diagram

        self._createApplicationMenuBar()
        self._createToolBar()
        self.SetTopWindow(self._frame)

        self._frame.SetAutoLayout(True)
        self._frame.Show(True)

        return True

    def _createApplicationMenuBar(self):

        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu = Menu()
        viewMenu: Menu = Menu()

        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")

        menuBar.Append(fileMenu, 'File')
        menuBar.Append(viewMenu, 'View')

        viewMenu.Append(id=self._ID_DISPLAY_RECTANGLE, item='Rectangle', helpString='Display a Rectangle')
        viewMenu.Append(id=self._ID_ROTATE_RECTANGLE,  item='Rotate',    helpString='Rotate Rectangle')

        self.Bind(EVT_MENU, self._onDisplayElement, id=self._ID_DISPLAY_RECTANGLE)
        self.Bind(EVT_MENU, self._onRotateElement,  id=self._ID_ROTATE_RECTANGLE)

        self._frame.SetMenuBar(menuBar)

    def _onDisplayElement(self, event: CommandEvent):
        menuId: int = event.GetId()
        match menuId:
            case self._ID_DISPLAY_RECTANGLE:
                self._displayRectangle()
            case _:
                self.logger.error(f'WTH!  I am not handling that menu item')

    # noinspection PyUnusedLocal
    def _onRotateElement(self, event: CommandEvent):
        self._rotatableShape.Rotate(clockwise=True)
        self._diagramFrame.Refresh()

    def _displayRectangle(self):

        rotatableShape: RotatableRectangle = RotatableRectangle()

        rotatableShape.draggable = True

        self._addToDiagram(rotatableShape=rotatableShape)

        self._rotatableShape = rotatableShape

    def _addToDiagram(self, rotatableShape: RotatableShape):

        x, y = self._getPosition()
        rotatableShape.SetPosition(x, y)
        self._diagramFrame.Refresh()

        self._diagram.AddShape(rotatableShape, withModelUpdate=True)

        self.logger.info(f'{self._diagram.GetShapes()=}')

    def _getPosition(self) -> Tuple[int, int]:
        x: int = self._x
        y: int = self._y

        self._x += INCREMENT_X
        self._y += INCREMENT_Y
        return x, y

    def _createToolBar(self):

        from wx import TB_HORIZONTAL
        from tests.demo.rotatable.icons.redCircle32 import embeddedImage as ImgCircle
        from tests.demo.rotatable.icons.ellipse32 import embeddedImage as ImgEllipse
        from tests.demo.rotatable.icons.polygon64 import embeddedImage as ImgPolygon
        from tests.demo.rotatable.icons.arc32 import embeddedImage as ImgArc

        nullBmp = BitmapBundle(NullBitmap)

        tb: ToolBar = self._frame.CreateToolBar(TB_HORIZONTAL | NO_BORDER | TB_FLAT)

        tb.SetSize((32, 32))

        """
        AddTool(toolId, label, bitmap, bmpDisabled, kind=ITEM_NORMAL, shortHelp=EmptyString, longHelp=EmptyString, clientData=None)
        """
        toolCircle: Bitmap      = ImgCircle.Bitmap
        circleId:   WindowIDRef = wxNewIdRef()
        tb.AddTool(circleId, 'Circle', toolCircle, nullBmp, ITEM_NORMAL, 'Circle', 'Long Help', 'Circle')

        toolEllipse: Bitmap      = ImgEllipse.Bitmap
        ellipseId:   WindowIDRef = wxNewIdRef()
        tb.AddTool(ellipseId, 'Ellipse', toolEllipse, nullBmp, ITEM_NORMAL, 'Ellipse', 'Long Help', 'Ellipse')

        toolPolygon: Bitmap      = ImgPolygon.Bitmap
        polygonId:   WindowIDRef = wxNewIdRef()
        tb.AddTool(polygonId, 'Polygon', toolPolygon, nullBmp, ITEM_NORMAL, 'Polygon', 'Long Help', 'Polygon')

        toolArc: Bitmap      = ImgArc.Bitmap
        arcId:   WindowIDRef = wxNewIdRef()
        tb.AddTool(arcId, 'Arc', toolArc, nullBmp, ITEM_NORMAL, 'Arc', 'Long Help', 'Arc')

        tb.AddSeparator()
        self._frame.SetToolBar(tb)
        tb.Realize()


if __name__ == '__main__':

    testApp: DemoRotatableShapes = DemoRotatableShapes()

    testApp.MainLoop()
