
from typing import NewType
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import DC
from wx import MouseEvent

from wx import PENSTYLE_LONG_DASH
from wx import Pen
from wx import RED
from wx import RED_PEN
from wx.core import LIGHT_GREY


from pyutmodelv2.PyutSDInstance import PyutSDInstance

from miniogl.AnchorPoint import AnchorPoint
from miniogl.LineShape import LineShape
from miniogl.MiniOglUtils import sign
from miniogl.Shape import Shape
from miniogl.ShapeEventHandler import ShapeEventHandler
from miniogl.SizerShape import SizerShape

from ogl.EventEngineMixin import EventEngineMixin

from ogl.preferences.OglPreferences import OglPreferences

from ogl.sd.OglInstanceNameV2 import OglInstanceNameV2
from ogl.sd.OglSDMessageV2 import OglSDMessages

InstanceSize = NewType('InstanceSize', Tuple[int, int])


class OglSDInstanceV2(Shape, ShapeEventHandler, EventEngineMixin):

    def __init__(self, pyutSDInstance: PyutSDInstance):

        self._v2Logger:        Logger         = getLogger(__name__)
        self._preferences:  OglPreferences = OglPreferences()

        self._instanceYPosition: int = self._preferences.instanceYPosition

        super().__init__()
        EventEngineMixin.__init__(self)

        self._pyutSDInstance: PyutSDInstance    = pyutSDInstance
        self._messages:       OglSDMessages     = OglSDMessages([])
        self._instanceName:   OglInstanceNameV2 = self._createInstanceName(pyutSDInstance=pyutSDInstance)
        self._lifeLine:       LineShape         = self._createLifeLine()

        self._clickedOnInstanceName: bool = False
        self._size:                  InstanceSize = InstanceSize((100, 400))
        self.visible = True

        #
        # TODO:  This will move to the mixin;  When I create it !!
        #
        self._topLeftSizer:  SizerShape = cast(SizerShape, None)
        self._topRightSizer: SizerShape = cast(SizerShape, None)
        self._botLeftSizer:  SizerShape = cast(SizerShape, None)
        self._botRightSizer: SizerShape = cast(SizerShape, None)

    @property
    def selected(self) -> bool:
        """
        Override Shape

        Returns: 'True' if selected 'False' otherwise
        """
        return self._selected

    @selected.setter
    def selected(self, state: bool):
        self._selected              = state
        self._instanceName.selected = state
        self._lifeLine.selected     = state
        self.ShowSizers(state)

    @property
    def pyutSDInstance(self):
        return self._pyutSDInstance

    @pyutSDInstance.setter
    def pyutSDInstance(self, pyutSDInstance: PyutSDInstance):
        self._pyutSDInstance = pyutSDInstance

    @property
    def messages(self) -> OglSDMessages:
        return self._messages

    def Draw(self, dc: DC, withChildren: bool = True):
        """
        Draw the shape.
        """
        self._v2Logger.debug(f'{self.GetSize()=}')
        super().Draw(dc=dc, withChildren=False)
        self.DrawChildren(dc)
        if self._selected is True:
            dc.SetPen(RED_PEN)
            self.DrawHandles(dc)

        self.DrawBorder(dc)

    def DrawBorder(self, dc):
        """
        Draw the border of the shape, for fast rendering.
        """
        super().DrawBorder(dc)
        savePen: Pen = dc.GetPen()

        if self._selected is True:
            drawPen: Pen = Pen(RED, style=PENSTYLE_LONG_DASH)
        else:
            drawPen = Pen(LIGHT_GREY, style=PENSTYLE_LONG_DASH)

        dc.SetPen(drawPen)

        sx, sy = self.GetPosition()
        sx = sx - self._ox
        sy = sy - self._oy
        width, height = self.GetSize()
        dc.DrawRectangle(sx, sy, width, height)

        dc.SetPen(savePen)

    def Inside(self, x, y) -> bool:
        if self._instanceName.Inside(x=x, y=y) is True:
            self._clickedOnInstanceName = True
            return True
        elif self._inside(x=x, y=y) is True:
            return True

        return False

    # noinspection PyUnusedLocal
    def OnLeftDown(self, event: MouseEvent):
        if self._clickedOnInstanceName is True:
            self._clickedOnInstanceName = False
            self._instanceName.selected = True

    def SetSize(self, width: int, height: int):
        """

        Args:
            width:
            height:
        """
        self._size = InstanceSize((width, height))

        self._instanceName.SetSize(width=100, height=height)

    def GetSize(self) -> InstanceSize:
        return self._size

    def ShowSizers(self, state: bool = True):
        """
        Show the four sizer shapes if state is True.

        TODO:  This is duplicated from RectangleShape.  Create a mixin to use for
        both.

        Args:
            state:

        """
        width, height = self.GetSize()
        if state and not self._topLeftSizer:
            self._topLeftSizer  = SizerShape(-self._ox, -self._oy, self)
            self._topRightSizer = SizerShape(-self._ox + width - 1, self._oy, self)
            self._botLeftSizer  = SizerShape(-self._ox, -self._oy + height - 1, self)
            self._botRightSizer = SizerShape(-self._ox + width - 1, -self._oy + height - 1, self)

            self._diagram.AddShape(self._topLeftSizer)
            self._diagram.AddShape(self._topRightSizer)
            self._diagram.AddShape(self._botLeftSizer)
            self._diagram.AddShape(self._botRightSizer)
        elif not state and self._topLeftSizer is not None:
            self._topLeftSizer.Detach()
            self._topRightSizer.Detach()
            self._botLeftSizer.Detach()
            self._botRightSizer.Detach()

            self._topLeftSizer  = cast(SizerShape, None)
            self._topRightSizer = cast(SizerShape, None)
            self._botLeftSizer  = cast(SizerShape, None)
            self._botRightSizer = cast(SizerShape, None)

    def addMessage(self, message):
        """
        Add a link to an ogl object.

        Args:
            message:  the message to add
        """
        self._messages.append(message)

    def _createInstanceName(self, pyutSDInstance: PyutSDInstance) -> OglInstanceNameV2:
        """

        Returns:  An OglInstanceName
        """
        text: str = self._pyutSDInstance.instanceName

        oglInstanceName: OglInstanceNameV2 = OglInstanceNameV2(pyutSDInstance, 0, 20, text, parent=self)
        oglInstanceName.SetRelativePosition(0, 0)

        self.AppendChild(oglInstanceName)

        return oglInstanceName

    def _createLifeLine(self) -> LineShape:
        """

        Returns:  The lifeline
        """
        width:   int = self._preferences.instanceDimensions.width
        height: int  = self._preferences.instanceDimensions.height
        (srcX, srcY, dstX, dstY) = (width // 2, 0,
                                    width // 2, height
                                    )

        srcY = srcY + self._instanceName.GetHeight()
        (src, dst) = (AnchorPoint(srcX, srcY, self), AnchorPoint(dstX, dstY, self))
        for el in [src, dst]:
            el.visible   = False
            el.draggable = False

        lifeLineShape: LineShape = LineShape(src, dst)

        lifeLineShape.parent    = self._instanceName
        lifeLineShape.drawArrow = False
        lifeLineShape.draggable = True
        lifeLineShape.pen       = BLACK_PEN
        lifeLineShape.visible   = True

        self.AppendChild(lifeLineShape)

        return lifeLineShape

    def _inside(self, x, y) -> bool:
        """
        True if (x, y) is inside the rectangle.

        TODO:  This is duplicated from RectangleShape;  Create a mixin to use for both

        Args:
            x:
            y:

        Returns:

        """
        # this also works if width and/or height is negative.
        sx, sy = self.GetPosition()
        # take a minimum of 4 pixels for the selection
        width, height = self.GetSize()
        width  = sign(width)  * max(abs(width),  4)
        height = sign(height) * max(abs(height), 4)
        topLeftX: int = sx - self._ox
        topLeftY: int = sy - self._oy

        topXLeftIsInside:  bool  = x >= topLeftX
        topXRightIsInside: bool  = x <= topLeftX + width
        topYLeftIsInside:  bool  = y >= topLeftY
        topYRightIsInside: bool  = y <= topLeftY + height
        if topXLeftIsInside and topXRightIsInside and topYLeftIsInside and topYRightIsInside:
            return True
        else:
            return False
