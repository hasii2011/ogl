
from typing import cast
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import Bitmap

from wx import ITEM_CHECK
from wx import ITEM_NORMAL
from wx import EVT_MENU

from wx import CommandEvent
from wx import MouseEvent
from wx import Menu
from wx import MenuItem

from pyutmodelv2.PyutClass import PyutClass

from pyutmodelv2.enumerations.PyutDisplayParameters import PyutDisplayParameters

if TYPE_CHECKING:
    from ogl.OglClass import OglClass

from ogl.OglConstants import OglConstants
from ogl.OglUtils import OglUtils

from ogl.events.IOglEventEngine import IOglEventEngine
from ogl.events.OglEvents import OglEventType

# Menu IDs
[
    MENU_TOGGLE_STEREOTYPE,
    MENU_TOGGLE_FIELDS,
    MENU_TOGGLE_METHODS,
    MENU_TOGGLE_METHOD_PARAMETERS,
    MENU_TOGGLE_CONSTRUCTOR,
    MENU_FIT_FIELDS,
    MENU_CUT_SHAPE,
    MENU_IMPLEMENT_INTERFACE
]  = OglUtils.assignID(8)

HELP_STEREOTYPE:  str = 'Set stereotype display on or off'
HELP_FIELDS:      str = 'Set fields display on or off'
HELP_METHODS:     str = 'Set methods display on or off'
HELP_PARAMETERS:  str = 'Set parameter display Unspecified, On or Off'
HELP_CONSTRUCTOR: str = 'Set constructor display Unspecified, On or Off'


@dataclass
class TriStateData:
    bitMap:   Bitmap
    menuText: str


class OglClassMenuHandler:
    def __init__(self, oglClass: 'OglClass', eventEngine: IOglEventEngine):

        self.logger: Logger = getLogger(__name__)

        self._oglClass:    'OglClass'        = oglClass
        self._eventEngine: IOglEventEngine = eventEngine

        self._contextMenu:       Menu     = cast(Menu, None)
        self._toggleStereotype:  MenuItem = cast(MenuItem, None)
        self._toggleFields:      MenuItem = cast(MenuItem, None)
        self._toggleMethods:     MenuItem = cast(MenuItem, None)
        self._toggleParameters:  MenuItem = cast(MenuItem, None)
        self._toggleConstructor: MenuItem = cast(MenuItem, None)

        self._createContextMenu()

    def popupMenu(self, event: MouseEvent):

        pyutClass: PyutClass = cast(PyutClass, self._oglClass.pyutObject)

        self._setMenuItemValues(pyutClass)

        x: int = event.GetX()
        y: int = event.GetY()
        self.logger.debug(f'OglClassMenuHandler - x,y: {x},{y}')

        # TODO:  Cheater, cheater pumpkin eater;  Have to fix this
        # noinspection PyProtectedMember
        frame = self._oglClass._diagram.GetPanel()
        frame.PopupMenu(self._contextMenu, x, y)

    def _createContextMenu(self):

        menu: Menu = Menu()

        self._toggleStereotype  = menu.Append(id=MENU_TOGGLE_STEREOTYPE,        item="Toggle stereotype display", helpString=HELP_STEREOTYPE,  kind=ITEM_CHECK)
        self._toggleFields      = menu.Append(id=MENU_TOGGLE_FIELDS,            item="Toggle fields display",     helpString=HELP_FIELDS,      kind=ITEM_CHECK)
        self._toggleMethods     = menu.Append(id=MENU_TOGGLE_METHODS,           item="Toggle methods display",    helpString=HELP_METHODS,     kind=ITEM_CHECK)
        self._toggleParameters  = menu.Append(id=MENU_TOGGLE_METHOD_PARAMETERS, item=" ",                         helpString=HELP_PARAMETERS,  kind=ITEM_NORMAL)
        self._toggleConstructor = menu.Append(id=MENU_TOGGLE_CONSTRUCTOR,       item=" ",                         helpString=HELP_CONSTRUCTOR, kind=ITEM_NORMAL)

        menu.Append(MENU_FIT_FIELDS,          'Fit Fields', 'Fit to see all class fields')
        menu.Append(MENU_CUT_SHAPE,           'Cut shape',  'Cut this shape')
        menu.Append(MENU_IMPLEMENT_INTERFACE, 'Implement Interface', 'Use Existing interface or create new one')

        # Callbacks
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_STEREOTYPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_METHODS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_FIT_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_CUT_SHAPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_IMPLEMENT_INTERFACE)
        menu.Bind(EVT_MENU, self.onDisplayParametersClick, id=MENU_TOGGLE_METHOD_PARAMETERS)

        self._contextMenu = menu

    def OnMenuClick(self, event: CommandEvent):
        """
        Callback for the popup menu on the class

        Args:
            event:
        """
        pyutClass: PyutClass = cast(PyutClass, self._oglClass.pyutObject)
        eventId:   int       = event.GetId()

        if eventId == MENU_TOGGLE_STEREOTYPE:
            pyutClass.displayStereoType = not pyutClass.displayStereoType
            self._oglClass.autoResize()
        elif eventId == MENU_TOGGLE_METHODS:
            pyutClass.showMethods = not pyutClass.showMethods     # flip it!!  too cute
            self._oglClass.autoResize()
        elif eventId == MENU_TOGGLE_FIELDS:
            pyutClass.showFields = not pyutClass.showFields       # flip it!! too cute
            self._oglClass.autoResize()
        elif eventId == MENU_FIT_FIELDS:
            self._oglClass.autoResize()
        elif eventId == MENU_CUT_SHAPE:
            self._eventEngine.sendEvent(OglEventType.CutOglClass, shapeToCut=self._oglClass)
        elif eventId == MENU_IMPLEMENT_INTERFACE:
            self._eventEngine.sendEvent(OglEventType.RequestLollipopLocation, requestShape=self._oglClass)
        else:
            event.Skip()

    # noinspection PyUnusedLocal
    def onDisplayParametersClick(self, event: CommandEvent):
        """
        This menu item has its own handler because this option is tri-state

        Unspecified --> Display --> Do Not Display ---|
            ^------------------------------------------|

        Args:
            event:
        """
        pyutClass:         PyutClass             = cast(PyutClass, self._oglClass.pyutObject)
        displayParameters: PyutDisplayParameters = pyutClass.displayParameters
        self.logger.debug(f'Current: {displayParameters=}')

        if displayParameters == PyutDisplayParameters.UNSPECIFIED:
            pyutClass.displayParameters = PyutDisplayParameters.WITH_PARAMETERS
        elif displayParameters == PyutDisplayParameters.WITH_PARAMETERS:
            pyutClass.displayParameters = PyutDisplayParameters.WITHOUT_PARAMETERS
        elif displayParameters == PyutDisplayParameters.WITHOUT_PARAMETERS:
            pyutClass.displayParameters = PyutDisplayParameters.UNSPECIFIED
        else:
            assert False, 'Unknown display type'
        self.logger.warning(f'New: {pyutClass.displayParameters=}')

    def _setMenuItemValues(self, pyutClass: PyutClass):

        self._toggleStereotype.Check(pyutClass.displayStereoType)
        self._toggleFields.Check(pyutClass.showFields)
        self._toggleMethods.Check(pyutClass.showMethods)

        self._setTheTriStateDisplayParametersMenuItem(pyutClass=pyutClass)

    def _setTheTriStateDisplayParametersMenuItem(self, pyutClass: PyutClass):

        displayParameters:    PyutDisplayParameters = pyutClass.displayParameters
        itemToggleParameters: MenuItem              = self._toggleParameters

        match displayParameters:
            case PyutDisplayParameters.UNSPECIFIED:
                triStateData: TriStateData = TriStateData(bitMap=OglConstants.unspecifiedDisplayMethodsIcon(), menuText='Unspecified Parameter Display')
            case PyutDisplayParameters.WITH_PARAMETERS:
                triStateData = TriStateData(bitMap=OglConstants.displayMethodsIcon(), menuText='Display Parameters')
            case PyutDisplayParameters.WITHOUT_PARAMETERS:
                triStateData = TriStateData(bitMap=OglConstants.doNotDisplayMethodsIcon(), menuText='Do Not Display Parameters')
            case _:
                self.logger.warning(f'Unknown Parameter DisplayType: {displayParameters}')
                assert False, 'Developer error'

        itemToggleParameters.SetBitmap(triStateData.bitMap)
        itemToggleParameters.SetItemLabel(triStateData.menuText)
