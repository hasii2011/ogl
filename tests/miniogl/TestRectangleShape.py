
from unittest import TestSuite
from unittest import main as unitTestMain

from tests.TestBase import TestBase

from miniogl.RectangleShape import RectangleShape

CANONICAL_X: int = 10
CANONICAL_Y: int = 10

CANONICAL_WIDTH:  int = 100
CANONICAL_HEIGHT: int = 100


class TestRectangleShape(TestBase):
    """
    """
    def setUp(self):
        super().setUp()

        self._rectangleShape: RectangleShape = RectangleShape(x=CANONICAL_X, y=CANONICAL_Y, width=CANONICAL_WIDTH, height=CANONICAL_HEIGHT, parent=None)

    def tearDown(self):
        super().tearDown()

    def testInsideTrue(self):

        actualAnswer: bool = self._rectangleShape.Inside(x=CANONICAL_X + 4, y=CANONICAL_Y + 6)

        self.assertTrue(actualAnswer, 'The point IS inside the rectangle')

    def testInsideFalseViaX(self):

        outsideX: int = CANONICAL_X + CANONICAL_WIDTH + 1

        actualAnswer: bool = self._rectangleShape.Inside(x=outsideX, y=CANONICAL_Y + 6)

        self.assertFalse(actualAnswer, 'The x-coordinate IS NOT inside the rectangle')

    def testInsideFalseViaY(self):

        outsideY: int = CANONICAL_Y + CANONICAL_HEIGHT + 1

        actualAnswer: bool = self._rectangleShape.Inside(x=CANONICAL_X + 4, y=outsideY)

        self.assertFalse(actualAnswer, 'The x-coordinate IS NOT inside the rectangle')


def suite() -> TestSuite:
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestRectangleShape))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
