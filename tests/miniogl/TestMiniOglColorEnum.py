
from unittest import TestSuite
from unittest import main as unitTestMain

from wx import Colour

from miniogl.MiniOglColorEnum import MiniOglColorEnum
from tests.ProjectTestBase import TestBase


class TestMiniOglColorEnum(TestBase):
    """
    """
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

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
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestMiniOglColorEnum))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
