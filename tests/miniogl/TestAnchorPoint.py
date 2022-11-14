
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from miniogl.Shape import Shape
from miniogl.AnchorPoint import AnchorPoint


class TestAnchorPoint(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):

        TestBase.setUpLogging()
        TestAnchorPoint.clsLogger = getLogger(__name__)

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.logger: Logger = TestAnchorPoint.clsLogger

        super().setUp()
        self.anchorPoint: AnchorPoint = AnchorPoint(x=93, y=276, parent=cast(Shape, None))

    def tearDown(self):
        super().tearDown()

    EXPECTED_X: int = 268
    EXPECTED_Y: int = 1044

    def testStayInside(self):
        x: int = 50
        y: int = 0
        topLeftX: float = TestAnchorPoint.EXPECTED_X
        topLeftY: float = TestAnchorPoint.EXPECTED_Y
        width:  float = 99.0
        height: float = 99.0

        adjustedX = self.anchorPoint.stayInside(low=topLeftX, length=width,  value=x)
        adjustedY = self.anchorPoint.stayInside(low=topLeftY, length=height, value=y)

        self.assertEqual(TestAnchorPoint.EXPECTED_X, adjustedX, 'Picked wrong X')
        self.assertEqual(TestAnchorPoint.EXPECTED_Y, adjustedY, 'Picked wrong Y')

        self.logger.info(f'Adjusted x,y: ({adjustedX},{adjustedY})')

    def testStickToBorder(self):
        """
        """
        topLeftX: float = TestAnchorPoint.EXPECTED_X
        topLeftY: float = TestAnchorPoint.EXPECTED_Y
        width:  float = 99.0
        height: float = 99.0

        # Simulate that call to .stayInside has returned adjustments
        adjustedX = TestAnchorPoint.EXPECTED_X
        adjustedY = TestAnchorPoint.EXPECTED_Y

        newX, newY = self.anchorPoint.stickToBorder(ox=topLeftX, oy=topLeftY, width=width, height=height, x=adjustedX, y=adjustedY)

        self.assertEqual(TestAnchorPoint.EXPECTED_X, newX, 'Picked wrong X')
        self.assertEqual(TestAnchorPoint.EXPECTED_Y, newY, 'Picked wrong Y')

        self.logger.info(f'stickToBorder newX,newY: ({newX},{newY})')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestAnchorPoint))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
