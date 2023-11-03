
from dataclasses import dataclass


@dataclass
class LabelPosition:
    x: int = 0
    y: int = 0


@dataclass
class LabelRelativePosition:
    x: int = 0
    y: int = 0


@dataclass
class OglAssociationLabelEventData:

    associationName:       str                   = ''
    associationId:         str                   = ''
    labelName:             str                   = ''
    labelId:               int                   = -1
    labelPosition:         LabelPosition         = LabelPosition(0, 0)
    labelRelativePosition: LabelRelativePosition = LabelRelativePosition(0, 0)
