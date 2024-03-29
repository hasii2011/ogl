from wx import Window

from wx.lib.sized_controls import SizedPanel

from ogl.preferences.OglPreferences import OglPreferences


class BaseOglPreferencesPage(SizedPanel):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self._preferences: OglPreferences = OglPreferences()

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
