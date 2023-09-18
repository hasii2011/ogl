
from dataclasses import dataclass
from dataclasses import field

from unittest import TestSuite
from unittest import main as unitTestMain

from codeallybasic.UnitTestBase import UnitTestBase

from miniogl.Common import Common


@dataclass
class Point:

    x: float = 0.0
    y: float = 0.0


def createOglPointFactory() -> Point:
    """
    """
    return Point(0, 0)


@dataclass
class TestLine:

    start: Point = field(default_factory=createOglPointFactory)
    end:   Point = field(default_factory=createOglPointFactory)


class TestMiniOglCommon(UnitTestBase):
    """
    """
    def setUp(self):
        super().setUp()
        self.common:   Common   = Common()
        self.testLine: TestLine = TestLine(start=Point(100, 100), end=Point(100, 200))

    def tearDown(self):
        super().tearDown()

    def testInsideSegment(self):

        clickPointX: float = 101.0
        clickPointY: float = 150.0

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideSegment(clickDiffStartX=clickDiffStartX, clickDiffStartY=clickDiffStartY, diffX=diffX, diffY=diffY)

        self.assertTrue(isIt, 'But, but it IS inside the segment')

    def testInsideSegmentFail(self):

        clickPointX: float = 100 + Common.CLICK_TOLERANCE + 1.0
        clickPointY: float = 150

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideSegment(clickDiffStartX=clickDiffStartX, clickDiffStartY=clickDiffStartY, diffX=diffX, diffY=diffY)

        self.assertFalse(isIt, 'But, but it IS NOT inside the segment')

    def testInsideBoundingBox(self):
        clickPointX: float = 101.0
        clickPointY: float = 150.0

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY)

        self.assertTrue(isIt, 'But, but it IS inside the bounding box')

    def testInsideBoundingBoxFalse(self):
        clickPointX: float = 100.0 + Common.CLICK_TOLERANCE
        clickPointY: float = 150.0

        x1: float = self.testLine.start.x
        y1: float = self.testLine.start.y
        x2: float = self.testLine.end.x
        y2: float = self.testLine.end.y

        diffX: float = x2 - x1
        diffY: float = y2 - y1

        clickDiffStartX: float = clickPointX - x1     # x - x1
        clickDiffStartY: float = clickPointY - y1     # y - y1

        isIt: bool = self.common.insideBoundingBox(clickDiffStartX, clickDiffStartY, diffX, diffY)

        self.assertFalse(isIt, 'But, but it IS NOT inside the bounding box')


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestMiniOglCommon))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
