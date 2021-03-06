
from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

from dataclasses import dataclass

from wx import BLACK
from wx import DC
from wx import EVT_MENU
from wx import FONTFAMILY_SWISS
from wx import FONTSTYLE_NORMAL
from wx import FONTWEIGHT_BOLD

from wx import Font
from wx import ClientDC
from wx import Menu
from wx import CommandEvent
from wx import MenuItem
from wx import MouseEvent
from wx import Point

from miniogl.SelectAnchorPoint import SelectAnchorPoint

from pyutmodel.PyutDisplayParameters import PyutDisplayParameters
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutObject import PyutObject
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutStereotype import PyutStereotype

from ogl.OglObject import OglObject
from ogl.OglObject import DEFAULT_FONT_SIZE

from ogl.OglConstants import OglConstants
from ogl.OglUtils import OglUtils
from ogl.events.OglEventType import OglEventType

from ogl.preferences.OglPreferences import OglPreferences

# Menu IDs
[
    MENU_TOGGLE_STEREOTYPE,
    MENU_TOGGLE_FIELDS,
    MENU_TOGGLE_METHODS,
    MENU_TOGGLE_METHOD_PARAMETERS,
    MENU_FIT_FIELDS,
    MENU_CUT_SHAPE,
    MENU_IMPLEMENT_INTERFACE
]  = OglUtils.assignID(7)

MARGIN: int = 10


@dataclass
class ClickedOnSelectAnchorPointData:
    clicked:           bool             = False
    selectAnchorPoint: SelectAnchorPoint = cast(SelectAnchorPoint, None)


class OglClass(OglObject):
    """
    OGL object that represents a UML class in class diagrams.
    This class defines OGL objects that represents a class. You can just
    instantiate an OGL class and add it to the diagram, links, resizing,
    ... are managed by parent class `OglObject`.

    For more instructions about how to create an OGL object, please refer
    to the `OglObject` class.
    """
    def __init__(self, pyutClass: PyutClass = None, w: int = 0, h: int = 0):
        """

        Args:
            pyutClass:  a PyutClass object
            w:  Width of the shape
            h:  Height of the shape
        """
        if pyutClass is None:
            pyutObject = PyutClass()
        else:
            pyutObject = pyutClass

        width:  int = w
        height: int = h

        self._oglPreferences: OglPreferences = OglPreferences()

        # Use preferences to get initial size if not specified
        # Note: auto_resize_shape_on_edit must be False for this size to actually stick
        if w == 0:
            width = self._oglPreferences.classDimensions.width
        if h == 0:
            height = self._oglPreferences.classDimensions.height

        super().__init__(pyutObject, width=width, height=height)

        self._nameFont: Font   = Font(DEFAULT_FONT_SIZE, FONTFAMILY_SWISS, FONTSTYLE_NORMAL, FONTWEIGHT_BOLD)
        self.logger:    Logger = getLogger(__name__)

    def handleSelectAnchorPointSelection(self, event: MouseEvent):
        """
        May be called (inexcusably bad form) by the selection anchor point left down handler
        by using its parent protected attribute

        Args:
            event:
        """
        self.logger.info(f'OnLeftDown: {event.GetPosition()}')
        # noinspection PyPropertyAccess
        clickPoint: Point = event.Position
        selectData: ClickedOnSelectAnchorPointData = self._didWeClickOnSelectAnchorPoint(clickPoint=clickPoint)
        if selectData.clicked is True:
            self.eventEngine.sendEvent(OglEventType.CreateLollipopInterface, implementor=self, attachmentPoint=selectData.selectAnchorPoint)

    def GetTextWidth(self, dc, text):
        width = dc.GetTextExtent(text)[0]
        return width

    def GetTextHeight(self, dc, text):
        height = dc.GetTextExtent(text)[1]
        return height

    def calculateClassHeader(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class header position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns:    tuple (x, y, w, h) = position and size of the header
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)
        # pyutObject = self.getPyutObject()
        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between text and line
        lth = dc.GetTextExtent("*")[1] // 2

        # from where begin the text
        h += lth

        # draw a pyutClass name
        name = self.pyutObject.name
        dc.SetFont(self._nameFont)
        nameWidth = self.GetTextWidth(dc, name)
        if draw:
            dc.DrawText(name, x + (w - nameWidth) // 2, y + h)
        if calcWidth:
            w = max(nameWidth, w)
        dc.SetFont(self._defaultFont)
        h += self.GetTextHeight(dc, str(name))
        h += lth

        # draw the stereotype if there's one
        pyutClass: PyutClass = self.pyutObject
        # stereo = self.getPyutObject().getStereotype()
        stereo: PyutStereotype = pyutClass.stereotype
        if stereo is not None and stereo.name != '' and pyutClass.getShowStereotype() is True:
            name = str(stereo)
            nameWidth = self.GetTextWidth(dc, name)
            if draw:
                dc.DrawText(name, x + (w - nameWidth) // 2, y + h)
            if calcWidth:
                w = max(nameWidth, w)
            h += self.GetTextHeight(dc, str(name))
            h += lth

        # Return sizes
        return x, y, w, h

    def calculateClassFields(self, dc, draw=False, initialX=None, initialY=None, calcWidth=False):
        """
        Calculate the class fields position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns:    tuple : (x, y, w, h) = position and size of the field
        """
        # Init
        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)

        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between text and line
        lth: int = dc.GetTextExtent("*")[1] // 2

        # Add space
        pyutClass: PyutClass = cast(PyutClass, self.pyutObject)
        if len(pyutClass.fields) > 0:
            h += lth

        # draw pyutClass fields
        if pyutClass.showFields is True:
            for field in pyutClass.fields:
                if draw:
                    dc.DrawText(str(field), x + MARGIN, y + h)
                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(field)))

                h += self.GetTextHeight(dc, str(field))

        # Add space
        if len(pyutClass.fields) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def calculateClassMethods(self, dc, draw=True, initialX=None, initialY=None, calcWidth=False) -> Tuple[int, int, int, int]:
        """
        Calculate the class methods position and size and display it if
        a draw is True

        Args:
            dc:
            draw:
            initialX:
            initialY:
            calcWidth:

        Returns:    tuple : (x, y, w, h) = position and size of the methods
        """

        dc.SetFont(self._defaultFont)
        dc.SetTextForeground(BLACK)

        x, y = self.GetPosition()
        if initialX is not None:
            x = initialX
        if initialY is not None:
            y = initialY
        w = self._width
        h = 0
        if calcWidth:
            w = 0

        # define space between text and line
        lth = dc.GetTextExtent("*")[1] // 2

        # Add space
        pyutClass: PyutClass = cast(PyutClass, self.pyutObject)
        if len(pyutClass.methods) > 0:
            h += lth

        # draw pyutClass methods
        self.logger.debug(f"showMethods => {pyutClass.showMethods}")
        if pyutClass.showMethods is True:
            for method in pyutClass.methods:
                if draw is True:
                    self.__drawMethodSignature(dc, method, pyutClass, x, y, h)

                if calcWidth:
                    w = max(w, self.GetTextWidth(dc, str(method)))

                h += self.GetTextHeight(dc, str(method))

        # Add space
        if len(pyutClass.methods) > 0:
            h += lth

        # Return sizes
        return x, y, w, h

    def Draw(self, dc, withChildren=False):
        """
        Paint handler, draws the content of the shape.

        WARNING : Every change here must be reported in autoResize pyutMethod

        Args:
            dc: device context to draw to
            withChildren:
        """

        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)

        # Draw rectangle shape
        OglObject.Draw(self, dc)

        # drawing is restricted in the specified region of the device
        w, h = self._width, self._height
        x, y = self.GetPosition()           # Get position
        dc.SetClippingRegion(x, y, w, h)

        # Draw header
        (headerX, headerY, headerW, headerH) = self.calculateClassHeader(dc, True)
        y = headerY + headerH

        if pyutObject.showFields is True:
            # Draw line
            dc.DrawLine(x, y, x + w, y)

            # Draw fields
            (fieldsX, fieldsY, fieldsW, fieldsH) = self.calculateClassFields(dc, True, initialY=y)
            y = fieldsY + fieldsH
        # Draw line
        dc.DrawLine(x, y, x + w, y)
        #
        # Method needs to be called even though returned values not used  -- TODO look at refactoring
        #
        if pyutObject.showMethods is True:
            (methodsX, methodsY, methodsW, methodsH) = self.calculateClassMethods(dc, True, initialY=y, calcWidth=True)
            # noinspection PyUnusedLocal
            y = methodsY + methodsH

        dc.DestroyClippingRegion()

    def autoResize(self):
        """
        Auto-resize the class

        WARNING : Every change here must be reported in DRAW pyutMethod
        """
        # Init
        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)
        umlFrame = self.GetDiagram().GetPanel()
        dc = ClientDC(umlFrame)

        # Get header size
        (headerX, headerY, headerW, headerH) = self.calculateClassHeader(dc, False, calcWidth=True)
        y = headerY + headerH

        # Get fields size
        if pyutObject.showFields is True:
            (fieldsX, fieldsY, fieldsW, fieldsH) = self.calculateClassFields(dc, False, initialY=y, calcWidth=True)
            y = fieldsY + fieldsH
        else:
            fieldsW, fieldsH = 0, 0

        # Get methods size
        if pyutObject.showMethods is True:
            (methodX, methodY, methodW, methodH) = self.calculateClassMethods(dc, True, initialY=y, calcWidth=True)
            y = methodY + methodH
        else:
            methodW, methodH = 0, 0

        w = max(headerW, fieldsW, methodW)
        h = y - headerY
        w += 2 * MARGIN
        self.SetSize(w, h)

        # to automatically replace the sizer objects at a correct place
        if self.IsSelected():
            self.SetSelected(False)
            self.SetSelected(True)

    def OnRightDown(self, event: MouseEvent):
        """
        Callback for right clicks
        """
        pyutObject: PyutClass = cast(PyutClass, self.pyutObject)
        menu:       Menu      = Menu()

        menu.Append(MENU_TOGGLE_STEREOTYPE, "Toggle stereotype display", "Set stereotype display on or off", True)
        item = menu.FindItemById(MENU_TOGGLE_STEREOTYPE)
        item.Check(pyutObject.getShowStereotype())

        menu.Append(MENU_TOGGLE_FIELDS, "Toggle fields display", "Set fields display on or off", True)
        item = menu.FindItemById(MENU_TOGGLE_FIELDS)
        item.Check(pyutObject.showFields)

        menu.Append(MENU_TOGGLE_METHODS, "Toggle methods display", "Set methods display on or off ", True)
        item = menu.FindItemById(MENU_TOGGLE_METHODS)
        item.Check(pyutObject.showMethods)

        menu.Append(MENU_TOGGLE_METHOD_PARAMETERS, "Toggle parameter display", "Set parameter display on or off", True)

        itemToggleParameters: MenuItem              = menu.FindItemById(MENU_TOGGLE_METHOD_PARAMETERS)
        displayParameters:    PyutDisplayParameters = self.pyutObject.displayParameters

        self._initializeTriStateDisplayParametersMenuItem(displayParameters, itemToggleParameters)

        menu.Append(MENU_FIT_FIELDS, "Fit Fields", "Fit to see all class fields")
        menu.Append(MENU_CUT_SHAPE,  "Cut shape",  "Cut this shape")

        menu.Append(MENU_IMPLEMENT_INTERFACE, 'Implement Interface', 'Use Existing interface or create new one')

        frame = self._diagram.GetPanel()

        # Callback
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_STEREOTYPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_TOGGLE_METHODS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_FIT_FIELDS)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_CUT_SHAPE)
        menu.Bind(EVT_MENU, self.OnMenuClick, id=MENU_IMPLEMENT_INTERFACE)
        menu.Bind(EVT_MENU, self.onDisplayParametersClick, id=MENU_TOGGLE_METHOD_PARAMETERS)

        x: int = event.GetX()
        y: int = event.GetY()
        self.logger.debug(f'OglClass - x,y: {x},{y}')
        frame.PopupMenu(menu, x, y)

    def OnMenuClick(self, event: CommandEvent):
        """
        Callback for popup menu on class

        Args:
            event:
        """
        pyutObject:   PyutClass = cast(PyutClass, self.pyutObject)
        eventId:      int       = event.GetId()

        if eventId == MENU_TOGGLE_STEREOTYPE:
            pyutObject.setShowStereotype(not pyutObject.getShowStereotype())
            self.autoResize()
        elif eventId == MENU_TOGGLE_METHODS:
            pyutObject.showMethods = not pyutObject.showMethods     # flip it!!  too cute
            self.autoResize()
        elif eventId == MENU_TOGGLE_FIELDS:
            pyutObject.showFields = not pyutObject.showFields       # flip it!! too cute
            self.autoResize()
        elif eventId == MENU_FIT_FIELDS:
            self.autoResize()
        elif eventId == MENU_CUT_SHAPE:
            self.eventEngine.sendEvent(OglEventType.CutOglClass, shapeToCut=self)
            # self.eventEngine.sendCutShapeEvent(shapeToCut=self)
        elif eventId == MENU_IMPLEMENT_INTERFACE:
            self.eventEngine.sendEvent(OglEventType.RequestLollipopLocation, requestShape=self)
            # self.eventEngine.sendRequestLollipopLocationEvent(requestShape=self)
        else:
            event.Skip()

    # noinspection PyUnusedLocal
    def onDisplayParametersClick(self, event: CommandEvent):
        """
        This menu item has its own handler because this option is tri-state

        Unspecified --> Display  --> Do Not Display ---|
            ^------------------------------------------|

        Args:
            event:
        """
        pyutClass:         PyutClass             = cast(PyutClass, self.pyutObject)
        displayParameters: PyutDisplayParameters = pyutClass.displayParameters
        self.logger.debug(f'Current: {displayParameters=}')

        if displayParameters == PyutDisplayParameters.UNSPECIFIED:
            pyutClass.displayParameters = PyutDisplayParameters.DISPLAY
        elif displayParameters == PyutDisplayParameters.DISPLAY:
            pyutClass.displayParameters = PyutDisplayParameters.DO_NOT_DISPLAY
        elif displayParameters == PyutDisplayParameters.DO_NOT_DISPLAY:
            pyutClass.displayParameters = PyutDisplayParameters.UNSPECIFIED
        else:
            assert False, 'Unknown display type'
        self.logger.warning(f'New: {pyutClass.displayParameters=}')

    def _didWeClickOnSelectAnchorPoint(self, clickPoint: Point) -> ClickedOnSelectAnchorPointData:
        """

        Args:
            clickPoint:

        Returns:  Data class with relevant information
        """
        from miniogl.Shape import Shape

        selectData: ClickedOnSelectAnchorPointData = ClickedOnSelectAnchorPointData(clicked=False)
        anchors = self.GetAnchors()
        for shape in anchors:
            child: Shape = cast(Shape, shape)
            if isinstance(child, SelectAnchorPoint):
                selectAnchorPoint: SelectAnchorPoint = cast(SelectAnchorPoint, child)
                x, y = clickPoint.Get()
                if selectAnchorPoint.Inside(x=x, y=y):
                    selectData.selectAnchorPoint = child
                    selectData.clicked           = True
                    break

        return selectData

    def _isSameName(self, other) -> bool:

        ans: bool = False
        selfPyutObj:  PyutObject = self.pyutObject
        otherPyutObj: PyutObject = other.pyutObject

        if selfPyutObj.name == otherPyutObj.name:
            ans = True
        return ans

    def _isSameId(self, other):

        ans: bool = False
        if self.GetID() == other.GetID():
            ans = True
        return ans

    def _initializeTriStateDisplayParametersMenuItem(self, displayParameters: PyutDisplayParameters, itemToggleParameters: MenuItem):

        if displayParameters == PyutDisplayParameters.UNSPECIFIED:
            itemToggleParameters.SetBitmap(OglConstants.unspecifiedDisplayMethodsIcon())
        elif displayParameters == PyutDisplayParameters.DISPLAY:
            itemToggleParameters.SetBitmap(OglConstants.displayMethodsIcon())
        elif displayParameters == PyutDisplayParameters.DO_NOT_DISPLAY:
            itemToggleParameters.SetBitmap(OglConstants.doNotDisplayMethodsIcon())
        else:
            assert False, 'Unknown display type'

    def __drawMethodSignature(self, dc: DC, pyutMethod: PyutMethod, pyutClass: PyutClass, x: int, y: int, h: int):
        """
        If preference is not set at individual class level defer to global; Otherwise,
        respect the class level preference

        Args:
            dc:
            pyutMethod:
            pyutClass:
            x:
            y:
            h:
        """
        self.logger.debug(f'{pyutClass.displayParameters=} - {self._oglPreferences.showParameters=}')
        if pyutClass.displayParameters == PyutDisplayParameters.UNSPECIFIED:
            if self._oglPreferences.showParameters is True:
                dc.DrawText(pyutMethod.methodWithParameters(), x + MARGIN, y + h)
            else:
                dc.DrawText(pyutMethod.methodWithoutParameters(), x + MARGIN, y + h)
        elif pyutClass.displayParameters == PyutDisplayParameters.DISPLAY:
            dc.DrawText(pyutMethod.methodWithParameters(), x + MARGIN, y + h)
        elif pyutClass.displayParameters == PyutDisplayParameters.DO_NOT_DISPLAY:
            dc.DrawText(pyutMethod.methodWithoutParameters(), x + MARGIN, y + h)
        else:
            assert False, 'Internal error unknown pyutMethod parameter display type'

    def __repr__(self):
        selfName:   str = self.pyutObject.name
        return f'OglClass.{selfName} id: {self.GetID()}'

    def __eq__(self, other) -> bool:

        if isinstance(other, OglClass):
            if self._isSameName(other) is True and self._isSameId(other) is True:
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):

        selfPyutObj:  PyutObject = self.pyutObject

        return hash(selfPyutObj.name) + hash(self.GetID())
