
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App

from tests.TestBase import TestBase

from ogl.OglClass import OglClass
from pyutmodel.PyutClass import PyutClass


class TestOglClass(TestBase):
    WELL_KNOWN_ID: int = 0xDeadBeef

    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglClass.clsLogger = getLogger(__name__)

    def setUp(self):
        self.app: App = App()

        self.logger: Logger = TestOglClass.clsLogger

    def tearDown(self):
        pass

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
