from typing import Callable
from typing import cast
from typing import List
from typing import NewType
from typing import Tuple

from logging import Logger
from logging import getLogger
from logging import DEBUG

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

from pyutmodel.PyutLink import PyutLink

from miniogl.LineShape import Segments
from miniogl.TextShape import TextShape

from ogl.OglAssociationLabel import OglAssociationLabel
from ogl.OglLink import OglLink
from ogl.OglPosition import OglPosition

from ogl.preferences.OglPreferences import OglPreferences

DiamondPoint  = NewType('DiamondPoint', Tuple[int, int])
DiamondPoints = NewType('DiamondPoints', List[DiamondPoint])

PI_6:         float = pi / 6


class OglAssociation(OglLink):

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

        self._associationNameLabel:   OglAssociationLabel = OglAssociationLabel(text=self._link.name, oglPosition=OglPosition(x=0, y=0))
        self._sourceCardinality:      OglAssociationLabel = OglAssociationLabel()
        self._destinationCardinality: OglAssociationLabel = OglAssociationLabel()

        self._defaultFont: Font = Font(self._preferences.associationTextFontSize, FONTFAMILY_DEFAULT, FONTSTYLE_NORMAL, FONTWEIGHT_NORMAL)

        self._associationNameTextShape:        TextShape = cast(TextShape, None)
        self._sourceCardinalityTextShape:      TextShape = cast(TextShape, None)
        self._destinationCardinalityTextShape: TextShape = cast(TextShape, None)

        self.SetDrawArrow(False)

    @property
    def pyutObject(self) -> PyutLink:
        """
        Override
        Returns:  The data model
        """
        return self._link

    @pyutObject.setter
    def pyutObject(self, pyutLink: PyutLink):
        """
        Override in order to update the UI
        Args:
            pyutLink:
        """
        self.oglAssociationLogger.debug(f'{pyutLink=}')
        self._link = pyutLink
        self.centerLabel.text            = pyutLink.name
        self.sourceCardinality.text      = pyutLink.sourceCardinality
        self.destinationCardinality.text = pyutLink.destinationCardinality

        self.oglAssociationLogger.debug(f'{self.centerLabel=}')

    @property
    def centerLabel(self) -> OglAssociationLabel:
        return self._associationNameLabel

    @centerLabel.setter
    def centerLabel(self, newValue: OglAssociationLabel):
        self._associationNameLabel = newValue

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

    def Draw(self, dc: DC, withChildren: bool = True):
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
        oglDp: OglPosition = self._computeDestinationPosition(sp=OglPosition.tupleToOglPosition(sp), dp=OglPosition.tupleToOglPosition(dp))

        if self._link.name != '' and self._associationNameTextShape is None:
            self._createAssociationName()
        elif self._associationNameTextShape is not None:
            self._updateAssociationState()

        if self._link.sourceCardinality != '' and self._sourceCardinalityTextShape is None:
            self._createSourceCardinality(sp=oglSp)
        elif self._sourceCardinalityTextShape is not None:
            self._updateSourceCardinalityState()

        if self._link.destinationCardinality != '' and self._destinationCardinalityTextShape is None:
            self._createDestinationCardinality(dp=oglDp)
        elif self._destinationCardinalityTextShape is not None:
            self._updateDestinationCardinalityState()

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

    def _createAssociationName(self):
        """
        Create association name text shape;
        """
        self._associationNameTextShape = self._createTextShapeFromAssociationLabel(associationLabel=self._associationNameLabel)

    def _createSourceCardinality(self, sp: OglPosition):

        self._sourceCardinalityTextShape = self._createTextShapeFromAssociationLabel(associationLabel=self._sourceCardinality)

        srcX, srcY = self._sourceCardinalityTextShape.ConvertCoordToRelative(x=sp.x, y=sp.y)
        self._sourceCardinalityTextShape.SetRelativePosition(x=srcX, y=srcY)
        self._sourceCardinality.oglPosition = OglPosition(x=srcX, y=srcY)

    def _createDestinationCardinality(self, dp: OglPosition):
        self._destinationCardinalityTextShape = self._createTextShapeFromAssociationLabel(associationLabel=self._destinationCardinality)

        dstX, dstY = self._destinationCardinalityTextShape.ConvertCoordToRelative(x=dp.x, y=dp.y)
        self._destinationCardinalityTextShape.SetRelativePosition(x=dstX, y=dstY)
        self._destinationCardinality.oglPosition = OglPosition(x=dstX, y=dstY)

    def _createTextShapeFromAssociationLabel(self, associationLabel: OglAssociationLabel) -> TextShape:

        oglPosition:    OglPosition = associationLabel.oglPosition
        labelTextShape: TextShape   = self._createTextShape(x=oglPosition.x, y=oglPosition.y, text=associationLabel.text, font=self._defaultFont)

        labelTextShape.draggable = True

        return labelTextShape

    def _updateAssociationState(self):

        x, y = self._associationNameTextShape.GetRelativePosition()

        self._associationNameLabel.oglPosition = OglPosition(x=x, y=y)
        self._associationNameTextShape.text = self._link.name

    def _updateSourceCardinalityState(self):
        x, y = self._sourceCardinalityTextShape.GetRelativePosition()

        self._sourceCardinality.oglPosition = OglPosition(x=x, y=y)
        self._sourceCardinalityTextShape.text = self._link.sourceCardinality

    def _updateDestinationCardinalityState(self):
        x, y = self._sourceCardinalityTextShape.GetRelativePosition()

        self.destinationCardinality.oglPosition = OglPosition(x=x, y=y)
        self._destinationCardinalityTextShape.text = self._link.destinationCardinality

    def _computeDestinationPosition(self, sp: OglPosition, dp: OglPosition) -> OglPosition:

        def computeDestination(dx, dy, linkLength) -> OglPosition:
            x: int = round((-20 * dx / linkLength + dx * 5 / linkLength) + dp.x)
            y: int = round((-20 * dy / linkLength - dy * 5 / linkLength) + dp.y)

            return OglPosition(x=x, y=y)

        return self._computePosition(sp=sp, dp=dp, calculatorFunction=computeDestination)

    def _computeSourcePosition(self, sp: OglPosition, dp: OglPosition) -> OglPosition:

        def computeSource(dx, dy, linkLength):
            x: int = round((20 * dx / linkLength - dx * 5 / linkLength) + sp.x)
            y: int = round((20 * dy / linkLength + dy * 5 / linkLength) + sp.y)

            return OglPosition(x=x, y=y)

        return self._computePosition(sp=sp, dp=dp, calculatorFunction=computeSource)

    def _computePosition(self, sp: OglPosition, dp: OglPosition, calculatorFunction: Callable) -> OglPosition:

        dx, dy            = self._computeDxDy(srcPosition=sp, destPosition=dp)
        linkLength: float = self._computeLinkLength(srcPosition=sp, destPosition=dp)

        oglPosition: OglPosition = calculatorFunction(dx, dy, linkLength)

        if self.oglAssociationLogger.isEnabledFor(DEBUG):
            info = (
                f'{sp=} '
                f'{dp=} '
                f'{dx=} '
                f'{dy=} '
                f'linkLength={linkLength:.2f} '
                f'{oglPosition=}'
            )
            self.oglAssociationLogger.debug(info)
        return oglPosition

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
