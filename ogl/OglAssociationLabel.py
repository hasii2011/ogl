from logging import Logger
from logging import getLogger

from wx import DC

from miniogl.TextShape import TextShape

from wx import Font


class OglAssociationLabel(TextShape):

    def __init__(self, x: int, y: int, text: str, parent=None, font: Font = None):

        super().__init__(x=x, y=y, text=text, parent=parent, font=font)

        self.labelLogger: Logger = getLogger(__name__)
        # self._oglPosition: OglPosition = OglPosition(x=x, y=x)
        """
        Saved relative position that is continually updated
        """

    def Draw(self, dc: DC, withChildren: bool = True):

        super().Draw(dc=dc, withChildren=withChildren)

        if self.IsMoving() is True:
            pos = self.GetPosition()
            rPos = self.GetRelativePosition()
            self.labelLogger.debug(f'{pos=} {rPos=}')
