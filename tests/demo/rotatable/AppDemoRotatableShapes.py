
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import App
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import DefaultPosition
from wx import EVT_MENU
from wx import ID_EXIT
from wx import Menu
from wx import MenuBar

from wx import Point
from wx import Size
from wx import ToolBar

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from miniogl.Diagram import Diagram

from tests.ProjectTestBase import ProjectTestBase

from tests.demo.rotatable.DemoRotatableShapeFrame import DemoRotatableShapeFrame
from tests.demo.rotatable.DemoToolBarHandler import DemoToolBarHandler
from tests.demo.rotatable.RotatableRectangle import RotatableRectangle

FRAME_WIDTH:  int = 800
FRAME_HEIGHT: int = 600

INITIAL_X:   int = 100
INITIAL_Y:   int = 100

INCREMENT_X: int = INITIAL_X + 20
INCREMENT_Y: int = INITIAL_Y + 100


class AppDemoRotatableShapes(App):
    def __init__(self):

        from tests.demo.rotatable.DemoRotatableShapeFrame import DemoRotatableShapeFrame

        ProjectTestBase.setUpLogging()

        self.logger: Logger = getLogger(__name__)

        self._frame:          SizedFrame              = cast(SizedFrame, None)
        self._diagramFrame:   DemoRotatableShapeFrame = cast(DemoRotatableShapeFrame, None)
        self._diagram:        Diagram                 = cast(Diagram, None)

        self._ID_DISPLAY_RECTANGLE: int = wxNewIdRef()
        self._ID_ROTATE_RECTANGLE:  int = wxNewIdRef()

        self._x: int = 200
        self._y: int = 200

        self._rotatableShape: RotatableRectangle = cast(RotatableRectangle, None)

        super().__init__(redirect=False)

    def OnInit(self):

        frameStyle:    int   = DEFAULT_FRAME_STYLE
        frameSize:     Size  = Size(width=FRAME_WIDTH, height=FRAME_HEIGHT)
        framePosition: Point = DefaultPosition

        self._frame = SizedFrame(parent=None, title="Test Rotatable Shapes", size=frameSize, pos=framePosition, style=frameStyle)
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

        viewMenu.Append(id=self._ID_ROTATE_RECTANGLE, item='Rotate', helpString='Rotate Rectangle')

        self.Bind(EVT_MENU, self._onRotateElement, id=self._ID_ROTATE_RECTANGLE)

        self._frame.SetMenuBar(menuBar)

    # noinspection PyUnusedLocal
    def _onRotateElement(self, event: CommandEvent):
        self._rotatableShape.Rotate(clockwise=True)
        self._diagramFrame.Refresh()

    def _createToolBar(self):

        handler: DemoToolBarHandler = DemoToolBarHandler(self._frame, diagramFrame=self._diagramFrame)

        toolBar: ToolBar = handler.toolbar
        self._frame.SetToolBar(toolBar)
        toolBar.Realize()


if __name__ == '__main__':

    testApp: AppDemoRotatableShapes = AppDemoRotatableShapes()

    testApp.MainLoop()
