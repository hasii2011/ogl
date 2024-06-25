
from logging import Logger
from logging import getLogger

from miniogl.rotatable.RotatableShape import RotatableShape
from miniogl.rotatable.VShapes import VCircle
from miniogl.rotatable.VShapes import VEllipse
from miniogl.rotatable.VShapes import VRectangle


class RotatableRectangle(RotatableShape):

    def __init__(self):

        self.rLogger: Logger = getLogger(__name__)
        super().__init__(x=100, y=120, width=225, height=225)

    def _defineShape(self):
        """
        This is the definition of the graphical object.
        It uses a list of basic shapes, that support rotation and scaling.
        Define your own shapes in children classes by filling the innermost
        list with `VShape` instances.
        """
        self._SHAPES = [
            [
                VRectangle(x=20,  y=20,  w=100, h=100),
                VEllipse(x=40,  y=40,  w=100, h=100),
                VCircle(x=80,  y=80,  r=50),
                VRectangle(x=100, y=100, w=100, h=100),
            ]
        ]

    def __repr__(self):
        return f'RotatableRectangle'

    def __str__(self):
        return self.__repr__()
