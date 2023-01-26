from typing import Tuple
from typing import cast

from logging import Logger
from logging import getLogger

import random

from pyutmodel.PyutField import PyutFields
from pyutmodel.PyutMethod import PyutMethods
from wx import App
from wx import CommandEvent
from wx import DEFAULT_FRAME_STYLE
from wx import EVT_MENU
from wx import ID_EXIT
from wx import Menu
from wx import MenuBar

from wx import NewIdRef as wxNewIdRef

from wx.lib.sized_controls import SizedFrame
from wx.lib.sized_controls import SizedPanel

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod
from pyutmodel.PyutMethod import PyutParameters
from pyutmodel.PyutParameter import PyutParameter
from pyutmodel.PyutStereotype import PyutStereotype
from pyutmodel.PyutText import PyutText
from pyutmodel.PyutType import PyutType
from pyutmodel.PyutVisibilityEnum import PyutVisibilityEnum

from miniogl.Diagram import Diagram
from ogl.OglClass import OglClass
from ogl.OglDimensions import OglDimensions
from ogl.OglObject import OglObject
from ogl.OglText import OglText

from ogl.events.IOglEventEngine import IEventEngine
from ogl.events.OglEventEngine import OglEventEngine
from ogl.preferences.OglPreferences import OglPreferences

from tests.TestBase import TestBase
from tests.demo.DemoUmlFrame import DemoUmlFrame

FRAME_WIDTH:  int = 800
FRAME_HEIGHT: int = 600

ZOOM_WIDTH:   int = FRAME_WIDTH - 100
ZOOM_HEIGHT:  int = FRAME_HEIGHT - 100

ZOOM_IN_UPPER_X: int = 0
ZOOM_IN_UPPER_Y: int = 0

ZOOM_OUT_X: int = ZOOM_WIDTH // 2
ZOOM_OUT_Y: int = ZOOM_HEIGHT // 2

INITIAL_X:   int = 100
INITIAL_Y:   int = 100

INCREMENT_X: int = INITIAL_X + 20
INCREMENT_Y: int = INITIAL_Y + 40


class TestOglElements(App):

    def __init__(self, redirect: bool):

        TestBase.setUpLogging()

        self.logger:          Logger          = getLogger(__name__)

        self._frame:          SizedFrame   = cast(SizedFrame, None)
        self._diagramFrame:   DemoUmlFrame = cast(DemoUmlFrame, None)
        self._diagram:        Diagram      = cast(Diagram, None)
        self._oglEventEngine: IEventEngine = cast(OglEventEngine, None)

        self._ID_DISPLAY_OGL_CLASS: int = wxNewIdRef()
        self._ID_DISPLAY_OGL_TEXT:  int = wxNewIdRef()
        self._ID_ZOOM_IN:           int = wxNewIdRef()
        self._ID_ZOOM_OUT:          int = wxNewIdRef()

        self._x: int = 100
        self._y: int = 100
        self._oglPreferences: OglPreferences = OglPreferences()

        super().__init__(redirect)

    def OnInit(self):
        self._frame = SizedFrame(parent=None, title="Test Ogl Elements", size=(FRAME_WIDTH, FRAME_HEIGHT), style=DEFAULT_FRAME_STYLE)
        self._frame.CreateStatusBar()  # should always do this when there's a resize border

        self._oglEventEngine = OglEventEngine(listeningWindow=self._frame)

        sizedPanel: SizedPanel = self._frame.GetContentsPane()
        self._diagramFrame = DemoUmlFrame(parent=sizedPanel, eventEngine=self._oglEventEngine)
        # noinspection PyUnresolvedReferences
        self._diagramFrame.SetSizerProps(expand=True, proportion=1)

        # Some incestuous behavior going on here
        self._diagram = Diagram(panel=self._diagramFrame)
        self._diagramFrame.diagram = self._diagram

        self._createApplicationMenuBar()

        self.SetTopWindow(self._frame)

        self._frame.SetAutoLayout(True)
        self._frame.Show(True)

        return True

    def _createApplicationMenuBar(self):

        menuBar:  MenuBar = MenuBar()
        fileMenu: Menu = Menu()
        viewMenu: Menu = Menu()

        fileMenu.AppendSeparator()
        fileMenu.Append(ID_EXIT, '&Quit', "Quit Application")

        viewMenu.Append(id=self._ID_DISPLAY_OGL_CLASS, item='Ogl Class', helpString='Display an Ogl Class')
        viewMenu.Append(id=self._ID_DISPLAY_OGL_TEXT,  item='Ogl Text',  helpString='Display Ogl Text')
        viewMenu.AppendSeparator()
        viewMenu.Append(id=self._ID_ZOOM_IN,  item='Zoom In',  helpString='Zoom the frame in')
        viewMenu.Append(id=self._ID_ZOOM_OUT, item='Zoom Out', helpString='Zoom the frame out')
        menuBar.Append(fileMenu, 'File')
        menuBar.Append(viewMenu, 'View')

        self._frame.SetMenuBar(menuBar)

        self.Bind(EVT_MENU, self._onDisplayElement, id=self._ID_DISPLAY_OGL_CLASS)
        self.Bind(EVT_MENU, self._onDisplayElement, id=self._ID_DISPLAY_OGL_TEXT)

        self.Bind(EVT_MENU, self._onZoom, id=self._ID_ZOOM_IN)
        self.Bind(EVT_MENU, self._onZoom, id=self._ID_ZOOM_OUT)

    def _onDisplayElement(self, event: CommandEvent):
        menuId: int = event.GetId()
        match menuId:
            case self._ID_DISPLAY_OGL_CLASS:
                self._displayOglClass()
            case self._ID_DISPLAY_OGL_TEXT:
                self._displayOglText()
            case _:
                self.logger.error(f'WTH!  I am not handling that menu item')

    def _onZoom(self, event: CommandEvent):
        menuId: int = event.GetId()

        if menuId == self._ID_ZOOM_IN:
            self._diagramFrame.DoZoomIn(ax=ZOOM_IN_UPPER_X, ay=ZOOM_IN_UPPER_Y, width=ZOOM_WIDTH, height=ZOOM_HEIGHT)
        elif menuId == self._ID_ZOOM_OUT:
            self._diagramFrame.DoZoomOut(ax=ZOOM_OUT_X, ay=ZOOM_OUT_Y)
        else:
            self.logger.error(f'Unknown Zoom menu id: {menuId}')

    def _displayOglText(self):
        pyutText: PyutText = PyutText(textContent=self._oglPreferences.textValue)
        textDimensions: OglDimensions = self._oglPreferences.textDimensions
        oglText:  OglText  = OglText(pyutText=pyutText, width=textDimensions.width, height=textDimensions.height)
        oglText.textFontFamily = self._oglPreferences.textFontFamily
        oglText.textSize       = self._oglPreferences.textFontSize
        oglText.isBold         = self._oglPreferences.textBold
        oglText.isItalicized   = self._oglPreferences.textItalicize

        self._addToDiagram(oglObject=oglText)
        oglText.autoResize()
        self._diagramFrame.Refresh()

    def _displayOglClass(self):

        pyutClass:     PyutClass  = PyutClass('DemoClass')
        pyutField:     PyutField  = PyutField(name='DemoField', visibility=PyutVisibilityEnum.PUBLIC,
                                              fieldType=PyutType('float'),
                                              defaultValue='42.0')

        if self._fiftyFifty() is True:
            pyutClass.stereotype = PyutStereotype.NO_STEREOTYPE
        else:
            pyutClass.stereotype = PyutStereotype.TYPE
        pyutParameter: PyutParameter = PyutParameter(name='DemoParameter', parameterType=PyutType("str"), defaultValue='Ozzee')
        pyutMethod:    PyutMethod    = PyutMethod(name='DemoMethod', visibility=PyutVisibilityEnum.PUBLIC)
        pyutMethod.parameters = PyutParameters([pyutParameter])

        pyutClass.fields  = PyutFields([pyutField])
        pyutClass.methods = PyutMethods([pyutMethod])
        classDimensions: OglDimensions = self._oglPreferences.classDimensions
        oglClass:  OglClass  = OglClass(pyutClass, w=classDimensions.width, h=classDimensions.height)

        self._addToDiagram(oglObject=oglClass)

    def _getPosition(self) -> Tuple[int, int]:
        x: int = self._x
        y: int = self._y

        self._x += INCREMENT_X
        self._y += INCREMENT_Y
        return x, y

    def _addToDiagram(self, oglObject: OglObject):

        oglObject.SetDraggable(True)
        x, y = self._getPosition()
        oglObject.SetPosition(x, y)
        self._diagram.AddShape(oglObject, withModelUpdate=True)
        self._diagramFrame.Refresh()

        self.logger.info(f'{self._diagram.GetShapes()=}')

    def _fiftyFifty(self) -> bool:
        if random.random() < .5:
            return True
        return False


testApp: TestOglElements = TestOglElements(redirect=False)

testApp.MainLoop()
