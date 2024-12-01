
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger

from wx import BLACK_PEN
from wx import DC
from wx import RED_PEN

from pyutmodelv2.PyutSDMessage import PyutSDMessage

from miniogl.LineShape import LineShape
from miniogl.AnchorPoint import AnchorPoint
from miniogl.TextShape import TextShape

from ogl.sd.OglSDInstanceV2 import OglSDInstanceV2

from ogl.OglPosition import OglPosition
from ogl.OglLink import OglLink


# TODO : Find a way to report moves from AnchorPoints to PyutSDMessage


class OglSDMessageV2(OglLink):
    """
    Class for a graphical message
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, srcSDInstance: OglSDInstanceV2, pyutSDMessage: PyutSDMessage, dstSDInstance: OglSDInstanceV2):
        """
        For this class use the .pyutSDMessage property to retrieve the data model

        Args:
            srcSDInstance:   Source shape OglSDInstance
            pyutSDMessage:  PyutSDMessage
            dstSDInstance:   Destination shape OglSDInstance

        """
        self._pyutSDMessage = pyutSDMessage

        super().__init__(srcShape=srcSDInstance, pyutLink=pyutSDMessage, dstShape=dstSDInstance)
        #
        # Override OglLink anchors
        #
        srcAnchor, dstAnchor = self._createAnchorPoints(srcShape=srcSDInstance, pyutSDMessage=pyutSDMessage, dstShape=dstSDInstance)
        srcAnchorPosition = srcAnchor.GetPosition()
        dstAnchorPosition = dstAnchor.GetPosition()

        self._srcAnchor: AnchorPoint = srcAnchor
        self._dstAnchor: AnchorPoint = dstAnchor

        oglSource:      OglPosition = OglPosition.tupleToOglPosition(srcAnchorPosition)
        oglDestination: OglPosition = OglPosition.tupleToOglPosition(dstAnchorPosition)
        linkLength: float = self._computeLinkLength(srcPosition=oglSource, destPosition=oglDestination)
        dx, dy            = self._computeDxDy(srcPosition=oglSource, destPosition=oglDestination)

        centerMessageX: int = round(-dy * 5 // linkLength)
        centerMessageY: int = round(dx * 5 // linkLength)

        self._messageLabel: TextShape = self.AddText(centerMessageX, centerMessageY, pyutSDMessage.message)  # font=self._defaultFont
        self.updateMessage()
        self.drawArrow = True

        assert isinstance(srcSDInstance, OglSDInstanceV2), 'Developer Error, src of message should be an instance'
        assert isinstance(dstSDInstance, OglSDInstanceV2), 'Developer Error, dst of message should be an instance'
        #
        # TODO:  Should I really do this?
        srcSDInstance.addMessage(self)
        dstSDInstance.addMessage(self)

    @property
    def pyutSDMessage(self) -> PyutSDMessage:
        """

        Returns: The pyut sd message
        """
        return self._pyutSDMessage

    def updatePositions(self):
        """
        Define the positions on lifeline (y)
        """
        src = self.sourceAnchor
        dst = self.destinationAnchor
        srcY = self._pyutSDMessage.sourceY      + src.parent.GetSegments()[0][1]
        dstY = self._pyutSDMessage.destinationY + dst.parent.GetSegments()[0][1]
        srcX = 0
        dstX = 0

        src.SetPosition(srcX, srcY)
        dst.SetPosition(dstX, dstY)

    def updateMessage(self):
        """
        Update the message
        """
        text:      str       = self._pyutSDMessage.message
        textShape: TextShape = self._messageLabel
        # Don't draw blank messages
        if text.strip() != "":
            textShape.text = text
            textShape.visible = True
        else:
            textShape.visible = False

    def Draw(self, dc: DC,  withChildren: bool = False):
        """
        Called for drawing the contents of links.

        Args:
            dc:     Device context
            withChildren:   `True` draw the children
        """
        self.updateMessage()

        srcAnchor, dstAnchor = self.getAnchors()

        srcX, srcY = srcAnchor.GetPosition()
        dstX, dstY = dstAnchor.GetPosition()

        if self._selected is True:
            dc.SetPen(RED_PEN)

        dc.DrawLine(srcX, srcY, dstX, dstY)
        self.DrawArrow(dc, srcAnchor.GetPosition(), dstAnchor.GetPosition())
        self.DrawChildren(dc=dc)

        dc.SetPen(BLACK_PEN)

    def Detach(self):
        """
        Override OglLink because are ends are OglSDInstance's
        """
        if self._diagram is not None and not self._protected:
            LineShape.Detach(self)
            self._srcAnchor.protected = False
            self._dstAnchor.protected = False
            self._srcAnchor.Detach()
            self._dstAnchor.Detach()

            self._detachFromOglEnds()
            # TODO:
            # pyutSDMessage: PyutSDMessage = self.pyutSDMessage
            # I don't think anything needs to be done because once
            # the Ogl instance is gone the model should disappear

    def _detachFromOglEnds(self):
        """
        Override base class
        """
        src: OglSDInstanceV2 = self.sourceShape
        dst: OglSDInstanceV2 = self.destinationShape
        assert isinstance(src, OglSDInstanceV2), 'Developer Error, src of message should be an instance'
        assert isinstance(dst, OglSDInstanceV2), 'Developer Error, dst of message should be an instance'

        links: List[OglSDMessageV2] = src.messages
        links.remove(self)

        links = dst.messages
        links.remove(self)

    def _createAnchorPoints(self, srcShape: OglSDInstanceV2, dstShape: OglSDInstanceV2,
                            pyutSDMessage: PyutSDMessage) -> Tuple[AnchorPoint, AnchorPoint]:
        """
        Royal ready to heat rice

        Args:
            dstShape:
            srcShape:
            pyutSDMessage

        Returns:  A tuple of anchor points for the source and destination shapes
        """
        srcY: int = pyutSDMessage.sourceY      - srcShape.lifeline.GetPosition()[1]
        dstY: int = pyutSDMessage.destinationY - dstShape.lifeline.GetPosition()[1]

        srcAnchor: AnchorPoint = srcShape.lifeline.AddAnchor(0, srcY)
        dstAnchor: AnchorPoint = dstShape.lifeline.AddAnchor(0, dstY)
        srcAnchor.SetStayOnBorder(False)
        dstAnchor.SetStayOnBorder(False)
        srcAnchor.SetStayInside(True)
        dstAnchor.SetStayInside(True)
        srcAnchor.visible = True
        dstAnchor.visible = True
        srcAnchor.draggable = True
        dstAnchor.draggable = True

        return srcAnchor, dstAnchor

    def __repr__(self) -> str:
        msg: str = self._pyutSDMessage.message
        return f'OglSDMessage[id: {self._id} {msg=}]'


OglSDMessagesV2 = NewType('OglSDMessagesV2', List[OglSDMessageV2])
