
from logging import Logger
from logging import getLogger

from miniogl.rotatable.RotatableShape import RotatableShape
from miniogl.rotatable.VShapes import VEllipticArc
from miniogl.rotatable.VShapes import VEllipticArcDetails
from miniogl.rotatable.VShapes import VPolygon
from miniogl.rotatable.VShapes import VShapePosition
from miniogl.rotatable.VShapes import VShapePositions


class RotatablePolygon(RotatableShape):

    def __init__(self):
        super().__init__(x=100, y=100, width=225, height=225)

        self.logger: Logger = getLogger(__name__)

    def _defineShape(self):
        """
        This is the definition of the graphical object.
        It uses a list of basic shapes, that support rotation and scaling.
        Define your own shapes in children classes by filling the innermost
        list with `VShape` instances.
        """
        vShapePositions: VShapePositions = VShapePositions(
            [
                VShapePosition(x=125, y=125),
                VShapePosition(x=150, y=125),
                VShapePosition(x=165, y=140),
                VShapePosition(x=135, y=175),
            ]
        )

        self._SHAPES = [
            [
                VPolygon(points=vShapePositions),
            ]
        ]

    def __repr__(self):
        return f'RotatableArc'

    def __str__(self):
        return self.__repr__()
