
from logging import Logger
from logging import getLogger

from miniogl.rotatable.RotatableShape import RotatableShape
from miniogl.rotatable.VShapes import VEllipticArc
from miniogl.rotatable.VShapes import VEllipticArcDetails


class RotatableEllipticArc(RotatableShape):

    def __init__(self):
        super().__init__(x=100, y=120, width=225, height=225)

        self.logger: Logger = getLogger(__name__)

    def _defineShape(self):
        """
        This is the definition of the graphical object.
        It uses a list of basic shapes, that support rotation and scaling.
        Define your own shapes in children classes by filling the innermost
        list with `VShape` instances.
        """
        self._SHAPES = [
            [
                VEllipticArc(VEllipticArcDetails(x=40, y=40, width=100, height=100, start=20, end=120)),
            ]
        ]

    def __repr__(self):
        return f'RotatableArc'

    def __str__(self):
        return self.__repr__()
