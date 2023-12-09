
from typing import Tuple
from typing import Union
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Brush
from wx import Pen
from wx import Window

from wx import Yield as wxYield

from pyutmodelv2.PyutModelTypes import ClassName
from pyutmodelv2.PyutInterface import PyutInterface

from miniogl.AttachmentSide import AttachmentSide
from miniogl.DiagramFrame import DiagramFrame
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglClass import OglClass
from ogl.OglInterface2 import OglInterface2
from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from ogl.events.IOglEventEngine import IOglEventEngine
from ogl.events.OglEvents import CreateLollipopInterfaceEvent
from ogl.events.OglEvents import DiagramFrameModifiedEvent
from ogl.events.OglEvents import EVT_CREATE_LOLLIPOP_INTERFACE
from ogl.events.OglEvents import EVT_DIAGRAM_FRAME_MODIFIED
from ogl.events.OglEvents import EVT_REQUEST_LOLLIPOP_LOCATION
from ogl.events.OglEvents import RequestLollipopLocationEvent

from tests.demo.DemoEventEngine import DemoEventEngine
from tests.demo.DemoEventEngine import DemoEventType


DEFAULT_WIDTH = 3000
A4_FACTOR:    float = 1.41

PIXELS_PER_UNIT_X: int = 20
PIXELS_PER_UNIT_Y: int = 20


class DemoUmlFrame(DiagramFrame):
    def __init__(self, parent: Window, demoEventEngine: DemoEventEngine):

        self.logger:           Logger          = getLogger(__name__)
        self._demoEventEngine: DemoEventEngine = demoEventEngine

        super().__init__(parent=parent)

        self.maxWidth:  int  = DEFAULT_WIDTH
        self.maxHeight: int = int(self.maxWidth / A4_FACTOR)  # 1.41 is for A4 support

        nbrUnitsX: int = int(self.maxWidth / PIXELS_PER_UNIT_X)
        nbrUnitsY: int = int(self.maxHeight / PIXELS_PER_UNIT_Y)
        initPosX:  int = 0
        initPosY:  int = 0
        self.SetScrollbars(PIXELS_PER_UNIT_X, PIXELS_PER_UNIT_Y, nbrUnitsX, nbrUnitsY, initPosX, initPosY, False)

        self._oglEventEngine.registerListener(event=EVT_REQUEST_LOLLIPOP_LOCATION, callback=self._onRequestLollipopLocation)
        self._oglEventEngine.registerListener(event=EVT_CREATE_LOLLIPOP_INTERFACE, callback=self._onCreateLollipopInterface)
        self._oglEventEngine.registerListener(event=EVT_DIAGRAM_FRAME_MODIFIED,    callback=self._onDiagramModified)

    @property
    def eventEngine(self) -> IOglEventEngine:
        return self._oglEventEngine

    def _onRequestLollipopLocation(self, event: RequestLollipopLocationEvent):

        shape = event.shape
        self._requestLollipopLocation(shape)

    def _onCreateLollipopInterface(self, event: CreateLollipopInterfaceEvent):

        attachmentPoint = event.attachmentPoint
        implementor     = event.implementor
        self.logger.info(f'{attachmentPoint=} {implementor=}')

        self._createLollipopInterface(self, implementor=implementor, attachmentAnchor=attachmentPoint)

    # noinspection PyUnusedLocal
    def _onDiagramModified(self, event: DiagramFrameModifiedEvent):
        """
        Catch the Ogl Event;  Let the application frame know about it
        Args:
            event:

        """
        self._demoEventEngine.sendEvent(eventType=DemoEventType.SET_STATUS_TEXT, statusMessage='Diagram Modified')

    def _createLollipopInterface(self, umlFrame: 'DemoUmlFrame', implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        pyutInterface: PyutInterface = PyutInterface(name='IGato')  # In real code invoke dialog

        pyutInterface.addImplementor(ClassName(implementor.pyutObject.name))

        oglInterface: OglInterface2 = OglInterface2(pyutInterface, attachmentAnchor)

        self._removeUnneededAnchorPoints(implementor, attachmentAnchor)

        anchorPosition: Tuple[int, int] = attachmentAnchor.GetPosition()
        self.logger.info(f'anchorPosition: {anchorPosition}')
        x = anchorPosition[0]
        y = anchorPosition[1]

        self.addShape(oglInterface, x, y, withModelUpdate=True)
        umlFrame.Refresh()

    def _requestLollipopLocation(self, destinationClass: OglClass):

        self._createPotentialAttachmentPoints(destinationClass=destinationClass)
        self._demoEventEngine.sendEvent(DemoEventType.SET_STATUS_TEXT, statusMessage='Select attachment point')

        self.Refresh()
        wxYield()

    def _createPotentialAttachmentPoints(self, destinationClass):

        dw, dh     = destinationClass.GetSize()

        southX = dw // 2        # do integer division
        southY = dh
        northX = dw // 2
        northY = 0
        westX  = 0
        westY  = dh // 2
        eastX  = dw
        eastY  = dh // 2

        self._createAnchorHints(destinationClass, southX, southY, AttachmentSide.SOUTH)
        self._createAnchorHints(destinationClass, northX, northY, AttachmentSide.NORTH)
        self._createAnchorHints(destinationClass, westX, westY, AttachmentSide.WEST)
        self._createAnchorHints(destinationClass, eastX, eastY, AttachmentSide.EAST)

    def _createAnchorHints(self, destinationClass: OglClass, anchorX: int, anchorY: int, attachmentSide: AttachmentSide):

        anchorHint: SelectAnchorPoint = SelectAnchorPoint(x=anchorX, y=anchorY, attachmentSide=attachmentSide, parent=destinationClass)
        anchorHint.SetProtected(True)

        destinationClass.AddAnchorPoint(anchorHint)
        self._diagram.AddShape(anchorHint)

    def _removeUnneededAnchorPoints(self, implementor: OglClass, attachmentAnchor: SelectAnchorPoint):

        attachmentSide: AttachmentSide = attachmentAnchor.attachmentPoint
        for iAnchor in implementor.GetAnchors():
            if isinstance(iAnchor, SelectAnchorPoint):
                anchor: SelectAnchorPoint = cast(SelectAnchorPoint, iAnchor)
                if anchor.attachmentPoint != attachmentSide:
                    anchor.SetProtected(False)
                    anchor.Detach()

    def addShape(self, shape: Union[OglObject, OglInterface2, SelectAnchorPoint, OglLink],
                 x: int, y: int, pen: Pen = None, brush: Brush = None, withModelUpdate: bool = True):
        """
        Add a shape to the UmlFrame.

        Args:
            shape: the shape to add
            x: coord of the center of the shape
            y: coord of the center of the shape
            pen: pen to use
            brush:  brush to use
            withModelUpdate: if true the model of the shape will update from the shape (view) when added to the diagram.
        """
        shape.SetDraggable(True)
        shape.SetPosition(x, y)
        if pen is not None:
            shape.SetPen(pen)
        if brush is not None:
            shape.SetBrush(brush)
        self._diagram.AddShape(shape, withModelUpdate)
