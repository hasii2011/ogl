
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger
from logging import INFO

from math import pi
from math import atan
from math import cos
from math import sin

from wx import BLACK_BRUSH
from wx import BLACK_PEN
from wx import DC
from wx import FONTFAMILY_DEFAULT
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_NORMAL
from wx import WHITE_BRUSH

from wx import Font

from miniogl.LineShape import Segments

from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglLink import OglLink
from ogl.OglPosition import OglPosition

from ogl.OglUtils import OglUtils
from ogl.preferences.OglPreferences import OglPreferences


# SegmentPoint  = NewType('SegmentPoint', Tuple[int, int])
# SegmentPoints = NewType('SegmentPoints', List[SegmentPoint])

DiamondPoint  = NewType('DiamondPoint', Tuple[int, int])
DiamondPoints = NewType('DiamondPoints', List[DiamondPoint])

PI_6:         float = pi / 6


class OglAssociation(OglLink):

    # TEXT_SHAPE_FONT_SIZE: int = 12
    clsDiamondSize: int = OglPreferences().associationDiamondSize
    """
    Graphical link representation of an association, (simple line, no arrow).
    To get a new link,  use the `OglLinkFactory` and specify
    the link type.  .e.g. OGL_ASSOCIATION for an instance of this class.
    """
    def __init__(self, srcShape, pyutLink, dstShape, srcPos=None, dstPos=None):
        """

        Args:
            srcShape:   Source shape
            pyutLink:   Conceptual links associated with the graphical links.
            dstShape:   Destination shape
            srcPos:     Position of source      Override location of input source
            dstPos:     Position of destination Override location of input destination
        """
        self.oglAssociationLogger: Logger         = getLogger(__name__)
        self._preferences:         OglPreferences = OglPreferences()

        super().__init__(srcShape, pyutLink, dstShape, srcPos=srcPos, dstPos=dstPos)

        self._centerLabel:            OglAssociationLabel = OglAssociationLabel()
        self._sourceCardinality:      OglAssociationLabel = OglAssociationLabel()
        self._destinationCardinality: OglAssociationLabel = OglAssociationLabel()

        self._defaultFont: Font = Font(self._preferences.associationTextFontSize, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        self.SetDrawArrow(False)

    @property
    def centerLabel(self) -> OglAssociationLabel:
        return self._centerLabel

    @centerLabel.setter
    def centerLabel(self, newValue: OglAssociationLabel):
        self._centerLabel = newValue

    @property
    def sourceCardinality(self) -> OglAssociationLabel:
        return self._sourceCardinality

    @sourceCardinality.setter
    def sourceCardinality(self, newValue: OglAssociationLabel):
        self._sourceCardinality = newValue

    @property
    def destinationCardinality(self) -> OglAssociationLabel:
        return self._destinationCardinality

    @destinationCardinality.setter
    def destinationCardinality(self, newValue: OglAssociationLabel):
        self._destinationCardinality = newValue

    def Draw(self, dc: DC, withChildren: bool = False):
        """
        Called to draw the link content.
        We are going to draw all of our stuff, cardinality, Link name, etc.

        Args:
            dc:     Device context
            withChildren:   draw the children or not
        """
        OglLink.Draw(self, dc, withChildren)
        sp: Tuple[int, int] = self._srcAnchor.GetPosition()
        dp: Tuple[int, int] = self._dstAnchor.GetPosition()

        oglSp: OglPosition = OglPosition(x=sp[0], y=sp[1])
        oglDp: OglPosition = OglPosition(x=dp[0], y=dp[1])

        self._drawSourceCardinality(dc=dc, sp=oglSp, dp=oglDp)
        self._drawCenterLabel(dc=dc, sp=oglSp, dp=oglDp)
        self._drawDestinationCardinality(dc=dc, sp=oglSp, dp=oglDp)

    def drawDiamond(self, dc: DC, filled: bool = False):
        """
        Draw an arrow at the beginning of the line.

        Args:
            dc:         The device context
            filled:     True if the diamond must be filled, False otherwise
        """
        #
        line: Segments = self.segments

        # self.oglAssociationLogger.debug(f'{line=}')
        points: DiamondPoints = OglAssociation.calculateDiamondPoints(lineSegments=line)
        # self.oglAssociationLogger.debug(f'{points:}')

        dc.SetPen(BLACK_PEN)
        if filled:
            dc.SetBrush(BLACK_BRUSH)
        else:
            dc.SetBrush(WHITE_BRUSH)
        dc.DrawPolygon(points)
        dc.SetBrush(WHITE_BRUSH)

    def _drawCenterLabel(self, dc: DC, sp: OglPosition, dp: OglPosition):

        segments = self.segments
        self.oglAssociationLogger.info(f'{segments=}')
        midPoint: OglPosition = OglUtils.computeMidPoint(srcPosition=sp, dstPosition=dp)

        saveFont: Font = dc.GetFont()
        dc.SetFont(self._defaultFont)

        centerText: str = self._link.name
        dc.DrawText(centerText, midPoint.x, midPoint.y)
        dc.SetFont(saveFont)
        self._centerLabel = self.__updateAssociationLabel(self._centerLabel, x=midPoint.x, y=midPoint.y, text=centerText)

    def _drawSourceCardinality(self, dc: DC, sp: OglPosition, dp: OglPosition):

        dx, dy            = self._computeDxDy(srcPosition=sp, destPosition=dp)

        linkLength: float = self._computeLinkLength(srcPosition=sp, destPosition=dp)

        srcLblX: int = round((20 * dx / linkLength - dx * 5 / linkLength) + sp.x)
        srcLblY: int = round((20 * dy / linkLength + dy * 5 / linkLength) + sp.y)

        if self.oglAssociationLogger.isEnabledFor(INFO):
            info = (
                f'{sp=} '
                f'{dp=} '
                f'{dx=} '
                f'{dy=} '
                f'linkLength={linkLength:.2f} '
                f'srcLblX={srcLblX:.2f} '
                f'srcLblY={srcLblY:.2f}'
            )
            self.oglAssociationLogger.debug(info)
        saveFont: Font = dc.GetFont()
        dc.SetFont(self._defaultFont)

        sourceCardinalityText: str = self._link.sourceCardinality
        dc.DrawText(sourceCardinalityText, srcLblX, srcLblY)
        dc.SetFont(saveFont)
        self._sourceCardinality = self.__updateAssociationLabel(self._sourceCardinality, x=srcLblX, y=srcLblY, text=sourceCardinalityText)

    def _drawDestinationCardinality(self, dc: DC, sp: OglPosition, dp: OglPosition):

        dx, dy            = self._computeDxDy(srcPosition=sp, destPosition=dp)

        linkLength: float = self._computeLinkLength(srcPosition=sp, destPosition=dp)

        dstLblX: int = round((-20 * dx / linkLength + dy * 5 / linkLength) + dp.x)
        dstLblY: int = round((-20 * dy / linkLength - dy * 5 / linkLength) + dp.y)

        saveFont: Font = dc.GetFont()
        dc.SetFont(self._defaultFont)

        destinationCardinalityText: str = self._link.destinationCardinality
        dc.DrawText(destinationCardinalityText, dstLblX, dstLblY)
        self._destinationCardinality = self.__updateAssociationLabel(self._destinationCardinality,
                                                                     x=dstLblX, y=dstLblY,
                                                                     text=destinationCardinalityText)
        dc.SetFont(saveFont)

    def __updateAssociationLabel(self, associationLabel: OglAssociationLabel, x: int, y: int, text: str) -> OglAssociationLabel:

        associationLabel.oglPosition.x = x
        associationLabel.oglPosition.y = y
        associationLabel.text          = text

        return associationLabel

    @staticmethod
    def calculateDiamondPoints(lineSegments: Segments) -> DiamondPoints:
        """
        Made static so that we can unit test it;  Please the only instance variables needed
        are passed in

        Args:
            lineSegments:  The line where we are putting the diamondPoints

        Returns:  The diamond points that define the diamond polygon
        """
        x1, y1 = lineSegments[1]
        x2, y2 = lineSegments[0]
        a: int = x2 - x1
        b: int = y2 - y1
        if abs(a) < 0.01:  # vertical segment
            if b > 0:
                alpha: float = -pi / 2
            else:
                alpha = pi / 2
        else:
            if a == 0:
                if b > 0:
                    alpha = pi / 2
                else:
                    alpha = 3 * pi / 2
            else:
                alpha = atan(b/a)
        if a > 0:
            alpha += pi
        alpha1: float = alpha + PI_6
        alpha2: float = alpha - PI_6

        diamondPoints: DiamondPoints = DiamondPoints([])

        dp0: DiamondPoint = OglAssociation.calculateDiamondPoint0(x2=x2, y2=y2, alpha1=alpha1)
        diamondPoints.append(dp0)

        diamondPoints.append(DiamondPoint((x2, y2)))

        dp2: DiamondPoint = OglAssociation.calculateDiamondPoint2(x2=x2, y2=y2, alpha2=alpha2)
        diamondPoints.append(dp2)

        dp3: DiamondPoint = OglAssociation.calculateDiamondPoint3(x2=x2, y2=y2, alpha=alpha)
        diamondPoints.append(dp3)

        return diamondPoints

    @classmethod
    def calculateDiamondPoint0(cls, x2: float, y2: float, alpha1: float) -> DiamondPoint:

        dpx0: float = x2 + OglAssociation.clsDiamondSize * cos(alpha1)
        dpy0: float = y2 + OglAssociation.clsDiamondSize * sin(alpha1)

        return DiamondPoint((round(dpx0), round(dpy0)))

    @classmethod
    def calculateDiamondPoint2(cls, x2: float, y2: float, alpha2: float) -> DiamondPoint:

        dpx2: float = x2 + OglAssociation.clsDiamondSize * cos(alpha2)
        dpy2: float = y2 + OglAssociation.clsDiamondSize * sin(alpha2)

        return DiamondPoint((round(dpx2), round(dpy2)))

    @classmethod
    def calculateDiamondPoint3(cls, x2: float, y2: float, alpha: float) -> DiamondPoint:

        dpx3: float = x2 + 2 * OglAssociation.clsDiamondSize * cos(alpha)
        dpy3: float = y2 + 2 * OglAssociation.clsDiamondSize * sin(alpha)

        return DiamondPoint((round(dpx3), round(dpy3)))

    def __repr__(self):
        return f'OglAssociation - {super().__repr__()}'
