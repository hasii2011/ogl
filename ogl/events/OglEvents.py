
from enum import Enum

from wx.lib.newevent import NewEvent

#
# Constructor returns a tuple; First is the event,  The second is the binder
#
ShapeSelectedEvent,   EVT_SHAPE_SELECTED   = NewEvent()
CutOglClassEvent,     EVT_CUT_OGL_CLASS    = NewEvent()
ProjectModifiedEvent, EVT_PROJECT_MODIFIED = NewEvent()

RequestLollipopLocationEvent, EVT_REQUEST_LOLLIPOP_LOCATION = NewEvent()
CreateLollipopInterfaceEvent, EVT_CREATE_LOLLIPOP_INTERFACE = NewEvent()


class OglEventType(Enum):
    """

    """

    ShapeSelected           = 'ShapeSelected'
    CutOglClass             = 'CutOglClass'
    ProjectModified         = 'ProjectModified'
    RequestLollipopLocation = 'RequestLollipopLocation'
    CreateLollipopInterface = 'CreateLollipopInterface'
