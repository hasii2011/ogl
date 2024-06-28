
from logging import Logger
from logging import getLogger

from miniogl.rotatable.RotatableShape import RotatableShape
from miniogl.rotatable.VShapes import VArc
from miniogl.rotatable.VShapes import VArcDetails


class RotatableArc(RotatableShape):

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
                VArc(VArcDetails(xStart=40, yStart=40, xEnd=80, yEnd=80, xCenter=60, yCenter=60)),
            ]
        ]

    def __repr__(self):
        return f'RotatableArc'

    def __str__(self):
        return self.__repr__()
