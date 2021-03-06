from logging import Logger
from logging import getLogger

from wx import WHITE_BRUSH

from miniogl.Shape import Shape

from pyutmodel.PyutLink import PyutLink
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink


class OglInheritance(OglLink):
    """
    Graphical OGL representation of an inheritance link.
    This class provide the methods for drawing an inheritance link between
    two classes of a UML diagram. Add labels to an OglLink.
    """
    def __init__(self, srcShape: OglClass, pyutLink: PyutLink, dstShape: OglClass, srcPos=None, dstPos=None):
        """

        Args:
            srcShape: Source shape
            pyutLink: Conceptual links associated with the graphical links.
            dstShape: Destination shape
            srcPos:   Position of source      Override location of input source
            dstPos:   Position of destination Override location of input destination
        """
        super().__init__(srcShape, pyutLink, dstShape, srcPos=srcPos, dstPos=dstPos)

        self.logger: Logger = getLogger(__name__)
        # Arrow must be white inside
        self.SetBrush(WHITE_BRUSH)
        self.SetDrawArrow(True)

    def __repr__(self):
        srcShape:  Shape = self.getSourceShape()
        dstShape: Shape  = self.getDestinationShape()
        sourceId:  int   = srcShape.GetID()
        dstId:    int    = dstShape.GetID()
        return f'OglInheritance[from: id: {sourceId} {self.getSourceShape()} to: id: {dstId} {self.getDestinationShape()}]'
