
from unittest import TestSuite
from unittest import main as unitTestMain

from hasiicommon.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodel.PyutClass import PyutClass

from ogl.OglClass import OglClass


class TestOglClass(UnitTestBaseW):
    WELL_KNOWN_ID: int = 0xDeadBeef

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testRepr(self):
        pyutClass: PyutClass = PyutClass(name='TestReprClass')
        pyutClass.id = TestOglClass.WELL_KNOWN_ID

        oglClass: OglClass = OglClass(pyutClass=pyutClass)

        expectedRepr: str = 'OglClass.TestReprClass modelId: 3735928559'
        actualRepr:   str = oglClass.__repr__()
        self.assertEqual(expectedRepr, actualRepr, 'Debug aid has changed')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglClass))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
