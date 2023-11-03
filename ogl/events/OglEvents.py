
from enum import Enum

from wx.lib.newevent import NewEvent

#
# Constructor returns a tuple; First is the event,  The second is the binder
#
ShapeSelectedEvent,        EVT_SHAPE_SELECTED   = NewEvent()
CutOglClassEvent,          EVT_CUT_OGL_CLASS    = NewEvent()
DiagramFrameModifiedEvent, EVT_DIAGRAM_FRAME_MODIFIED = NewEvent()

RequestLollipopLocationEvent, EVT_REQUEST_LOLLIPOP_LOCATION = NewEvent()
CreateLollipopInterfaceEvent, EVT_CREATE_LOLLIPOP_INTERFACE = NewEvent()

DebugOglAssociationLabelEvent, EVT_DEBUG_OGL_ASSOCIATION_LABEL = NewEvent()


class OglEventType(Enum):
    """

    """

    ShapeSelected           = 'ShapeSelected'
    CutOglClass             = 'CutOglClass'
    DiagramFrameModified    = 'DiagramFrameModified'
    RequestLollipopLocation = 'RequestLollipopLocation'
    CreateLollipopInterface = 'CreateLollipopInterface'

    DebugOglAssociationLabel = 'DebugOglAssociationLabel'
