
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from miniogl.MiniOglPenStyle import MiniOglPenStyle

from wx import CB_READONLY
from wx import EVT_CHECKBOX
from wx import EVT_CHOICE
from wx import EVT_COMBOBOX
from wx import EVT_SPINCTRL

from wx import CheckBox
from wx import Choice
from wx import ComboBox
from wx import SpinCtrl
from wx import SpinEvent
from wx import CommandEvent
from wx import Window

from wx.lib.sized_controls import SizedPanel
from wx.lib.sized_controls import SizedStaticBox

from ogl.preferences.OglPreferences import OglPreferences


SPINNER_WIDTH:  int = 60
SPINNER_HEIGHT: int = 35


class DiagramPreferencesPage(SizedPanel):
    """
    This is a complex layout.  The following description is good as of version 0.60.50;
    If you change the layout please update this (Yeah, I do not like this kind of brittle
    documentation either

        ----------------- Dialog Sized Panel --------------------------------------------------------------------------------------------------------
        |                                                                                                                                           |
        |   ----------------- HorizontalPanel ---------------------------------------------------------------------------------------------         |
        |  |     ------------------- Vertical Panel --------------   ------------------- gridIntervalSSB -------------------              |         |
        |  |     |                                               |   |                                                      |             |         |
        |  |     |                                               |   |                                                      |             |         |
        |  |     |                                               |   |                                                      |             |         |
        |  |     |                                               |   |                                                      |             |         |
        |  |     |                                               |   |                                                      |             |         |
        |  |     -------------------------------------------------   --------------------------------------------------------             |         |
        |  --------------------------------------------------------------------------------------------------------------------------------         |
        |                                                                                                                                           |
        |   ------------------------------------------gridPanel-------------------------------------------------------------------                  |
        |  |                                                                                                                     |                  |
        |  |    ---------- gridLineColorSSB ------------------     ---------- gridLineStyleSSB ------------------                |                  |
        |  |    |                                             |   |                                             |                |                  |
        |  |    |                                             |   |                                             |                |                  |
        |  |    |                                             |   |                                             |                |                  |
        |  |    |                                             |   |                                             |                |                  |
        |  |    |                                             |   |                                             |                |                  |
        |  |    |                                             |   |                                             |                |                  |
        |  |    ---------- gridLineColorSSB ------------------     ---------- gridLineStyleSSB ------------------                |                  |
        |  |                                                                                                                     |                  |
        |  |                                                                                                                     |                  |
        |   ----------------------------------------------------------------------------------------------------------------------                  |
        |                                                                                                                                           |
        |                                                                                                                                           |
        ----------------- Dialog Sized Panel --------------------------------------------------------------------------------------------------------

    """

    def __init__(self, parent: Window):

        self.logger: Logger = getLogger(__name__)

        super().__init__(parent)
        self.SetSizerType('vertical')

        self._preferences: OglPreferences = OglPreferences()

        self._enableBackgroundGrid: CheckBox = cast(CheckBox, None)
        self._snapToGrid:           CheckBox = cast(CheckBox, None)
        self._gridInterval:         SpinCtrl = cast(SpinCtrl, None)
        self._gridLineColor:        ComboBox = cast(ComboBox, None)
        self._gridStyleChoice:      Choice   = cast(Choice, None)
        self._layoutControls(self)
        self._setControlValues()
        self._bindCallbacks(parent=self)

    def _layoutControls(self, parentSizedPanel: SizedPanel):

        horizontalPanel: SizedPanel = SizedPanel(parentSizedPanel)
        verticalPanel:   SizedPanel = SizedPanel(horizontalPanel)
        horizontalPanel.SetSizerType('horizontal')
        horizontalPanel.SetSizerProps(expand=True, proportion=3)
        verticalPanel.SetSizerType('vertical')

        self._enableBackgroundGrid = CheckBox(verticalPanel, label='Enable Background Grid')
        self._snapToGrid           = CheckBox(verticalPanel, label='Snap Shapes to Grid')

        self._layoutGridIntervalControl(horizontalPanel)

        self._layoutGridOptions(panel=parentSizedPanel)

        self._fixPanelSize(panel=self)

    @property
    def name(self) -> str:
        return 'Diagram'

    def _setControlValues(self):
        """
        """
        self._resetSnapToGridControl()

        self._enableBackgroundGrid.SetValue(self._preferences.backgroundGridEnabled)
        self._snapToGrid.SetValue(self._preferences.snapToGrid)
        self._gridInterval.SetValue(self._preferences.backgroundGridInterval)
        self._gridLineColor.SetValue(self._preferences.gridLineColor.value)

        gridLineStyles: List[str] = self._gridStyleChoice.GetItems()
        selectedIndex:  int       = gridLineStyles.index(self._preferences.gridLineStyle.value)
        self._gridStyleChoice.SetSelection(selectedIndex)

    def _bindCallbacks(self, parent):

        parent.Bind(EVT_CHECKBOX, self._onEnableBackgroundGridChanged,   self._enableBackgroundGrid)
        parent.Bind(EVT_CHECKBOX, self._onSnapToGridChanged,             self._snapToGrid)
        parent.Bind(EVT_COMBOBOX, self._onGridLineColorSelectionChanged, self._gridLineColor)
        parent.Bind(EVT_SPINCTRL, self._onGridIntervalChanged,           self._gridInterval)
        parent.Bind(EVT_CHOICE,   self._onGridStyleChanged,              self._gridStyleChoice)

    def _layoutGridIntervalControl(self, sizedPanel):
        gridIntervalSSB: SizedStaticBox = SizedStaticBox(sizedPanel, label='Grid Interval')
        gridIntervalSSB.SetSizerProps(expand=True)
        self._gridInterval = SpinCtrl(parent=gridIntervalSSB)

    def _layoutGridOptions(self, panel: SizedPanel):

        gridPanel: SizedPanel = SizedPanel(panel)
        gridPanel.SetSizerType('horizontal')
        gridPanel.SetSizerProps(expand=True, proportion=2)

        self._createGridLineColorControl(panel=gridPanel)
        self._createGridStyleChoice(panel=gridPanel)

    def _createGridLineColorControl(self, panel: SizedPanel):

        colorChoices = []
        for cc in MiniOglColorEnum:
            colorChoices.append(cc.value)

        gridLineColorSSB: SizedStaticBox = SizedStaticBox(panel, label='Grid Line Color')
        gridLineColorSSB.SetSizerProps(expand=True, proportion=1)

        self._gridLineColor = ComboBox(gridLineColorSSB, choices=colorChoices, style=CB_READONLY)

    def _createGridStyleChoice(self, panel: SizedPanel):

        gridStyles = [s.value for s in MiniOglPenStyle]

        gridLineStyleSSB: SizedStaticBox = SizedStaticBox(panel, label='Grid Line Style')
        gridLineStyleSSB.SetSizerProps(expand=True, proportion=1)

        self._gridStyleChoice = Choice(gridLineStyleSSB, choices=gridStyles)

    def _onEnableBackgroundGridChanged(self, event: CommandEvent):

        enabledValue: bool = event.IsChecked()
        self.logger.warning(f'onEnableBackgroundGridChanged - {enabledValue=}')
        self._preferences.backgroundGridEnabled = enabledValue
        self._resetSnapToGridControl()

    def _onSnapToGridChanged(self, event: CommandEvent):

        enabledValue: bool = event.IsChecked()
        self.logger.info(f'onSnapToGridChanged - {enabledValue=}')
        self._preferences.snapToGrid = enabledValue
        event.Skip(True)

    def _onGridLineColorSelectionChanged(self, event: CommandEvent):

        colorValue:    str              = event.GetString()
        pyutColorEnum: MiniOglColorEnum = MiniOglColorEnum(colorValue)

        self._preferences.gridLineColor = pyutColorEnum

    def _onGridIntervalChanged(self, event: SpinEvent):

        newInterval: int = event.GetInt()
        self._preferences.backgroundGridInterval = newInterval

    def _onGridStyleChanged(self, event: CommandEvent):

        styleText: str = event.GetString()
        self.logger.warning(f'{styleText=}')

        pyutPenStyle: MiniOglPenStyle = MiniOglPenStyle(styleText)

        self._preferences.gridLineStyle = pyutPenStyle

    def _resetSnapToGridControl(self):
        """
        Make the UI consistent when the background grid is used or not
        If no background grid there is nothing to snap to
        """
        if self._preferences.backgroundGridEnabled is True:
            self._snapToGrid.Enabled = True
        else:
            self._snapToGrid.SetValue(False)
            self._snapToGrid.Enabled = False
            self._preferences.snapToGrid = False

    def _fixPanelSize(self, panel: SizedPanel):
        """
        Do the following or does not get resized correctly
        A little trick to make sure that the sizer cannot be resized to
        less screen space than the controls need

        Args:
            panel:
        """
        panel.Fit()
        panel.SetMinSize(panel.GetSize())
