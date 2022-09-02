
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from ogl.OglAssociation import DiamondPoints
from ogl.OglAssociation import SegmentPoint
from ogl.OglAssociation import SegmentPoints
from tests.TestBase import TestBase

from ogl.OglAssociation import OglAssociation


class TestOglAssociation(TestBase):
    """
    You need to change the name of this class to Test`xxxx`
    Where `xxxx' is the name of the class that you want to test.

    See existing tests for more information.
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglAssociation.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglAssociation.clsLogger

    def tearDown(self):
        pass

    def testCalculateDiamondPointsHorizontalLine(self):
        """
        Simple test of static method
        """
        segmentPoint0: SegmentPoint = SegmentPoint((547, 172))
        segmentPoint1: SegmentPoint = SegmentPoint((722, 173))
        segmentPoint2: SegmentPoint = SegmentPoint((723, 300))

        lineSegments:  SegmentPoints = SegmentPoints([segmentPoint0, segmentPoint1, segmentPoint2])

        diamondPoints: DiamondPoints = OglAssociation.calculateDiamondPoints(lineSegments=lineSegments)

        self.logger.debug(f'{diamondPoints}')

        self.assertEqual(553, diamondPoints[0][0], '')
        self.assertEqual(176, diamondPoints[0][1], '')

        self.assertEqual(547, diamondPoints[1][0], '')
        self.assertEqual(172, diamondPoints[1][1], '')

        self.assertEqual(553, diamondPoints[2][0], '')
        self.assertEqual(169, diamondPoints[2][1], '')

        self.assertEqual(561, diamondPoints[3][0], '')
        self.assertEqual(172, diamondPoints[3][1], '')

    def testCalculateDiamondPointsVerticalLine(self):
        segmentPoint0: SegmentPoint = SegmentPoint((505, 243))
        segmentPoint1: SegmentPoint = SegmentPoint((506, 425))

        lineSegments:  SegmentPoints = SegmentPoints([segmentPoint0, segmentPoint1])

        diamondPoints: DiamondPoints = OglAssociation.calculateDiamondPoints(lineSegments=lineSegments)

        self.logger.debug(f'{diamondPoints}')

        self.assertEqual(502., diamondPoints[0][0], '')
        self.assertEqual(249, diamondPoints[0][1], '')

        self.assertEqual(505, diamondPoints[1][0], '')
        self.assertEqual(243, diamondPoints[1][1], '')

        self.assertEqual(509, diamondPoints[2][0], '')
        self.assertEqual(249, diamondPoints[2][1], '')

        self.assertEqual(505, diamondPoints[3][0], '')
        self.assertEqual(257, diamondPoints[3][1], '')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglAssociation))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
