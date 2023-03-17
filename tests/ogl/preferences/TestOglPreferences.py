
from typing import cast

from logging import Logger
from logging import getLogger

from os import remove as osRemove
from os import path as osPath

from shutil import copyfile

from unittest import TestCase

from unittest import TestSuite
from unittest import main as unitTestMain

from miniogl.MiniOglPenStyle import MiniOglPenStyle
from ogl.OglDimensions import OglDimensions
from tests.TestBase import TestBase

from ogl.preferences.OglPreferences import OglPreferences

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class TestOglPreferences(TestCase):
    """
    """
    BACKUP_SUFFIX: str = '.backup'

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglPreferences.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglPreferences.clsLogger
        self.oglPreferences: OglPreferences = OglPreferences()

        self._backupPrefs()

    def tearDown(self):
        self._restoreBackup()

    def testInitialCreation(self):
        """
        Make sure we correctly create the preferences file if none exists
        It must have the default values
        """
        self.logger.warning(f'testInitialCreation -- not yet implemented')

    def testNewOglPreferences(self):

        oglPreferences: OglPreferences = OglPreferences()
        self.assertIsNotNone(oglPreferences, 'For some reason instantiation did not work')

    def testChangeNoteText(self):

        self.oglPreferences.noteText = 'I changed it'
        actualNoteText: str = self.oglPreferences.noteText
        self.assertEqual('I changed it', actualNoteText, 'Hmm did not change')

    def testChangeClassDimensions(self):
        self.oglPreferences.classDimensions = OglDimensions(width=100, height=100)
        actualDimensions: OglDimensions = self.oglPreferences.classDimensions
        self.assertEqual(OglDimensions(100, 100), actualDimensions, 'Ouch did not change')

    def testChangeDefaultMethodName(self):
        self.oglPreferences.methodName = 'I changed you'
        actualName: str = self.oglPreferences.methodName
        self.assertEqual('I changed you', actualName, 'The default method name did not change')

    def testChangeGridLineStyle(self):
        self.oglPreferences.gridLineStyle = MiniOglPenStyle.CROSS_HATCH
        actualStyle: MiniOglPenStyle = self.oglPreferences.gridLineStyle
        self.assertEqual(MiniOglPenStyle.CROSS_HATCH, actualStyle, 'Grid line style did not change')

    def testTwoColorValue(self):

        self._createDefaultPreferences()
        self.prefs.init()  # reload default prefs
        expectedColor: str = OglPreferences.DEFAULT_GRID_LINE_COLOR
        actualColor:   str = self.prefs.gridLineColor.value

        self.assertEqual(expectedColor, actualColor, 'Default must have changed')

    def _backupPrefs(self):

        prefsFileName: str = self.oglPreferences._preferencesFileName
        original: str = prefsFileName
        backup:   str = f"{prefsFileName}{TestOglPreferences.BACKUP_SUFFIX}"
        if osPath.exists(original):
            try:
                copyfile(original, backup)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

    def _restoreBackup(self):

        prefsFileName: str = self.oglPreferences._preferencesFileName
        backup:   str = f"{prefsFileName}{TestOglPreferences.BACKUP_SUFFIX}"
        original: str = prefsFileName
        if osPath.exists(backup):
            try:
                copyfile(backup, original)
            except IOError as e:
                self.logger.error(f"Unable to copy file. {e}")

            osRemove(backup)
        else:
            osRemove(original)

    def _createDefaultPreferences(self):
        """
        Delete the file and force creation of a default one
        """
        prefsFileName: str = self.oglPreferences._preferencesFileName

        osRemove(prefsFileName)
        self.prefs: OglPreferences = OglPreferences()


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
