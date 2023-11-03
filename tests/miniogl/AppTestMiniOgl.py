from wx import App
from wx import BITMAP_TYPE_PNG
from wx import Bitmap
from wx import Button
from wx import ClientDC
from wx import CommandEvent

from wx import DEFAULT_FRAME_STYLE
from wx import EVT_BUTTON
from wx import Frame
from wx import Image
from wx import MemoryDC
from wx import NullBitmap
from wx import ScrolledWindow
# noinspection PyProtectedMember
from wx._core import BitmapType

from miniogl.DiagramFrame import DiagramFrame
from miniogl.Diagram import Diagram
from miniogl.LollipopLine import LollipopLine

from miniogl.PointShape import PointShape
from miniogl.RectangleShape import RectangleShape
from miniogl.AnchorPoint import AnchorPoint
from miniogl.LineShape import LineShape
from miniogl.ControlPoint import ControlPoint
from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.AttachmentSide import AttachmentSide


class AppTestMiniOglApp(App):

    FRAME_ID:      int = 0xDeadBeef
    WINDOW_WIDTH:  int = 900
    WINDOW_HEIGHT: int = 500

    def OnInit(self):

        frameTop: Frame = Frame(parent=None, id=AppTestMiniOglApp.FRAME_ID, title="Test MiniOgl",
                                size=(AppTestMiniOglApp.WINDOW_WIDTH, AppTestMiniOglApp.WINDOW_HEIGHT), style=DEFAULT_FRAME_STYLE)
        frameTop.Show(True)

        diagramFrame: DiagramFrame = DiagramFrame(frameTop)
        diagramFrame.SetSize((AppTestMiniOglApp.WINDOW_WIDTH, AppTestMiniOglApp.WINDOW_HEIGHT))
        diagramFrame.SetScrollbars(10, 10, 100, 100)

        button = Button(frameTop, 1003, "Draw Me")
        button.SetPosition((15, 15))
        self.Bind(EVT_BUTTON, self.onDrawMe, button)

        diagramFrame.Show(True)

        self.SetTopWindow(diagramFrame)

        # noinspection PyAttributeOutsideInit
        self._diagramFrame: DiagramFrame = diagramFrame

        self.initTest()

        return True

    def initTest(self):

        diagramFrame: Diagram = self._diagramFrame.diagram

        pointShape: PointShape = PointShape(50, 50)
        diagramFrame.AddShape(pointShape)

        for x in range(10):
            for y in range(3):
                pointShape = PointShape(300 + x*50, 300 + y*50)
                diagramFrame.AddShape(pointShape)

        rectShape: RectangleShape = RectangleShape(100, 50, 130, 80)
        rectShape.SetDraggable(True)
        diagramFrame.AddShape(rectShape)

        anchor1 = AnchorPoint(50, 100, None)
        anchor1.SetDraggable(True)
        anchor2 = AnchorPoint(200, 300, None)
        anchor2.SetDraggable(True)

        lineShape: LineShape = LineShape(anchor1, anchor2)
        lineShape.SetDrawArrow(False)
        lineShape.draggable = True
        lineShape.SetSpline(False)

        controlPoint: ControlPoint = ControlPoint(50, 150, None)
        lineShape.AddControl(controlPoint, None)
        controlPoint = ControlPoint(200, 150, None)
        lineShape.AddControl(controlPoint, None)

        diagramFrame.AddShape(lineShape)

        self.drawLollipops()

    def drawLollipops(self):

        diagramFrame: Diagram = self._diagramFrame.diagram

        rectShape: RectangleShape = RectangleShape(400, 50, 130, 80)
        rectShape.draggable = True
        diagramFrame.AddShape(rectShape)

        dw, dh     = rectShape.GetSize()

        eastX, eastY   = dw, dh // 2

        dstAnchor = SelectAnchorPoint(parent=rectShape, attachmentSide=AttachmentSide.EAST, x=eastX, y=eastY)
        dstAnchor.draggable = False

        lollipopLine: LollipopLine = LollipopLine(dstAnchor)

        diagramFrame.AddShape(lollipopLine)

    # noinspection PyUnusedLocal
    def onDrawMe(self, event: CommandEvent):

        extension: str = 'png'
        imageType: BitmapType = BITMAP_TYPE_PNG
        window: ScrolledWindow = self._diagramFrame
        context: ClientDC = ClientDC(window)
        memory: MemoryDC = MemoryDC()

        x, y = window.ClientSize
        emptyBitmap: Bitmap = Bitmap(x, y, -1)

        memory.SelectObject(emptyBitmap)
        memory.Blit(source=context, xsrc=0, height=y, xdest=0, ydest=0, ysrc=0, width=x)
        memory.SelectObject(NullBitmap)

        img: Image = emptyBitmap.ConvertToImage()
        filename: str = f'DiagramDump.{extension}'
        status: bool = img.SaveFile(filename, imageType)


testApp: App = AppTestMiniOglApp(redirect=False)

testApp.MainLoop()
