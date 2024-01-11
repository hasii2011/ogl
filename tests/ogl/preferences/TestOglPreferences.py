
from os import environ as osEnvironment

from pathlib import Path

from unittest import TestSuite

from unittest import main as unitTestMain

from codeallybasic.ConfigurationLocator import XDG_CONFIG_HOME_ENV_VAR

from codeallybasic.UnitTestBase import UnitTestBase

from miniogl.MiniOglPenStyle import MiniOglPenStyle

from ogl.OglDimensions import OglDimensions

from ogl.preferences.OglPreferences import OglPreferences


class TestOglPreferences(UnitTestBase):
    """
    """
    BACKUP_SUFFIX: str = '.backup'

    def setUp(self):
        super().setUp()
        """
        Create a fake location since we know that the configuration
        locator favors using the XDG environment variable
        """
        fakeXDGPATH: Path = Path('/tmp/fakeXDG/.config')

        osEnvironment[XDG_CONFIG_HOME_ENV_VAR] = fakeXDGPATH.as_posix()

        self.oglPreferences: OglPreferences = OglPreferences()

    def tearDown(self):
        """
        Hook method for deconstructing the class fixture after running all tests in the class.
        """
        preferenceFile: Path = self.oglPreferences._preferencesFileName
        preferenceFile.unlink(missing_ok=True)

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

        expectedColor: str = OglPreferences.DEFAULT_GRID_LINE_COLOR
        actualColor:   str = self.oglPreferences.gridLineColor.value

        self.assertEqual(expectedColor, actualColor, 'Default must have changed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglPreferences))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
