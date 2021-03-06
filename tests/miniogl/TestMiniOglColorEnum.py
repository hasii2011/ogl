
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from wx import App
from wx import Colour

from miniogl.MiniOglColorEnum import MiniOglColorEnum

from tests.TestBase import TestBase


class TestMiniOglColorEnum(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestMiniOglColorEnum.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestMiniOglColorEnum.clsLogger
        self.app            = App()

    def tearDown(self):
        self.app.OnExit()
        del self.app

    def testBlack(self):
        c: Colour = MiniOglColorEnum.toWxColor(MiniOglColorEnum.BLACK)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Black should be a valid color')

    def testLightGrey(self):
        c: Colour = MiniOglColorEnum.toWxColor(MiniOglColorEnum.LIGHT_GREY)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Light Grey should be a valid color')

    def testCornFlowerBlue(self):
        c: Colour = MiniOglColorEnum.toWxColor(MiniOglColorEnum.CORNFLOWER_BLUE)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Corn Flower Blue should be a valid color')

    def testYellow(self):
        c: Colour = MiniOglColorEnum.toWxColor(MiniOglColorEnum.YELLOW)
        self.assertTrue(c.IsOk(), 'Wah, wah.  Yellow should be a valid color')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestMiniOglColorEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
