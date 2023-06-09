
from dataclasses import dataclass
from dataclasses import field

from ogl.OglPosition import OglPosition


def createOglPosition() -> OglPosition:
    return OglPosition(x=0, y=0)


@dataclass
class OglAssociationLabel:

    text:        str         = ''
    oglPosition: OglPosition = field(default_factory=createOglPosition)
