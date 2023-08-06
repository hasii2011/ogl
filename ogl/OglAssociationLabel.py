
from miniogl.TextShape import TextShape

from wx import Font

from ogl.OglPosition import OglPosition


class OglAssociationLabel(TextShape):

    def __init__(self, x: int, y: int, text: str, parent=None, font: Font = None):

        super().__init__(x=x, y=y, text=text, parent=parent, font=font)

        self._oglPosition: OglPosition = OglPosition(x=x, y=x)
        """
        Saved relative position that is continually updated
        """
