
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.enumerations.PyutDisplayMethods import PyutDisplayMethods

from ogl.OglClass import OglClass


class TestOglClass(UnitTestBaseW):
    WELL_KNOWN_ID: int = 0xDeadBeef

    def setUp(self):
        super().setUp()

        pyutClass: PyutClass = PyutClass(name='TestReprClass')
        pyutClass.id = TestOglClass.WELL_KNOWN_ID

        self._oglClass: OglClass = OglClass(pyutClass=pyutClass)

    def tearDown(self):
        super().tearDown()

    def testRepr(self):

        oglClass: OglClass = self._oglClass

        expectedRepr: str = 'OglClass.TestReprClass modelId: 3735928559'
        actualRepr:   str = oglClass.__repr__()
        self.assertEqual(expectedRepr, actualRepr, 'Debug aid has changed')

    def testAllowMethodDeferGlobalTrue(self):

        oglClass: OglClass = self._oglClass

        actualAnswer: bool = oglClass._allowDraw(classProperty=PyutDisplayMethods.UNSPECIFIED, globalValue=True)

        self.assertTrue(actualAnswer, 'Did not defer to global value')

    def testAllowMethodDeferGlobalFalse(self):

        oglClass: OglClass = self._oglClass

        actualAnswer: bool = oglClass._allowDraw(classProperty=PyutDisplayMethods.UNSPECIFIED, globalValue=False)

        self.assertFalse(actualAnswer, 'Did not defer to global value')

    def testAllowMethodLocalIsTrue(self):

        oglClass: OglClass = self._oglClass

        actualAnswer: bool = oglClass._allowDraw(classProperty=PyutDisplayMethods.DISPLAY, globalValue=True)

        self.assertTrue(actualAnswer, 'Did not defer to class value')

    def testAllowMethodLocalIsFalse(self):

        oglClass: OglClass = self._oglClass

        actualAnswer: bool = oglClass._allowDraw(classProperty=PyutDisplayMethods.DO_NOT_DISPLAY, globalValue=True)

        self.assertFalse(actualAnswer, 'Did not defer to class value')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglClass))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
