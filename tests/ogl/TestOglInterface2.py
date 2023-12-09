
from typing import Tuple

from unittest import TestSuite
from unittest import main as unitTestMain

from unittest.mock import Mock
from unittest.mock import PropertyMock

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodelv2.PyutInterface import PyutInterface

from miniogl.SelectAnchorPoint import SelectAnchorPoint
from miniogl.AttachmentSide import AttachmentSide

from ogl.OglInterface2 import OglInterface2
from ogl.OglPosition import OglPosition


class TestOglInterface2(UnitTestBaseW):
    """
    """
    def setUp(self):
        super().setUp()
        self._pyutInterface:    PyutInterface     = PyutInterface()
        self._destinationAnchor: SelectAnchorPoint = SelectAnchorPoint(250, 250, AttachmentSide.NORTH, None)

    def tearDown(self):
        super().tearDown()

    def testEqual(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface,  destinationAnchor=self._destinationAnchor)
        # noinspection SpellCheckingInspection
        doppleGanger: OglInterface2 = oglInterface

        self.assertEqual(oglInterface, doppleGanger, 'Magic method __equ__ does not appear to be working anymore')

    def testHash(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        currentHash: int = oglInterface.__hash__()
        hashAgain:   int = oglInterface.__hash__()

        self.assertEqual(currentHash, hashAgain, '__hash__ seems to be broken')

    def testInterfaceNameEast(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        pixelSize: Tuple[int, int] = (6, 12)
        textSize:  Tuple[int, int] = (80, 12)
        mockDestinationAnchor: Mock = Mock()

        type(mockDestinationAnchor).attachmentPoint    = PropertyMock(return_value=AttachmentSide.EAST)
        mockDestinationAnchor.GetPosition.return_value = (437, 144)

        namePosition: OglPosition = oglInterface._determineInterfaceNamePosition(mockDestinationAnchor, pixelSize=pixelSize, textSize=textSize)

        self.assertIsNotNone(namePosition, 'Minimally return an object')
        self.assertEqual(485, namePosition.x, 'East name position X is bad')
        self.assertEqual(120, namePosition.y, 'East name position Y is bad')

    def testInterfaceNameWest(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        pixelSize: Tuple[int, int] = (6, 12)
        textSize:  Tuple[int, int] = (107, 12)
        mockDestinationAnchor: Mock = Mock()

        type(mockDestinationAnchor).attachmentPoint    = PropertyMock(return_value=AttachmentSide.WEST)
        mockDestinationAnchor.GetPosition.return_value = (735, 275)

        namePosition: OglPosition = oglInterface._determineInterfaceNamePosition(mockDestinationAnchor, pixelSize=pixelSize, textSize=textSize)

        self.assertIsNotNone(namePosition, 'Minimally return an object')
        self.assertEqual(622, namePosition.x, 'West name position X is bad')
        self.assertEqual(251, namePosition.y, 'West name position Y is bad')

    def testInterfaceNameNorth(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        pixelSize: Tuple[int, int] = (6, 12)
        textSize:  Tuple[int, int] = (109, 12)
        mockDestinationAnchor: Mock = Mock()

        type(mockDestinationAnchor).attachmentPoint    = PropertyMock(return_value=AttachmentSide.NORTH)
        mockDestinationAnchor.GetPosition.return_value = (248, 315)

        namePosition: OglPosition = oglInterface._determineInterfaceNamePosition(mockDestinationAnchor, pixelSize=pixelSize, textSize=textSize)

        self.assertIsNotNone(namePosition, 'Minimally return an object')
        self.assertEqual(194, namePosition.x, 'West name position X is bad')
        self.assertEqual(237, namePosition.y, 'West name position Y is bad')

    def testInterfaceNameSouth(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        pixelSize: Tuple[int, int] = (6, 12)
        textSize:  Tuple[int, int] = (111, 12)
        mockDestinationAnchor: Mock = Mock()

        type(mockDestinationAnchor).attachmentPoint    = PropertyMock(return_value=AttachmentSide.SOUTH)
        mockDestinationAnchor.GetPosition.return_value = (738, 451)

        namePosition: OglPosition = oglInterface._determineInterfaceNamePosition(mockDestinationAnchor, pixelSize=pixelSize, textSize=textSize)

        self.assertIsNotNone(namePosition, 'Minimally return an object')
        self.assertEqual(683, namePosition.x, 'South name position X is bad')
        self.assertEqual(525, namePosition.y, 'South name position Y is bad')

    def testInterfaceNameWestOverSizeName(self):

        oglInterface: OglInterface2 = OglInterface2(pyutInterface=self._pyutInterface, destinationAnchor=self._destinationAnchor)

        pixelSize: Tuple[int, int] = (6, 12)
        textSize:  Tuple[int, int] = (135, 12)
        mockDestinationAnchor: Mock = Mock()

        type(mockDestinationAnchor).attachmentPoint    = PropertyMock(return_value=AttachmentSide.WEST)
        mockDestinationAnchor.GetPosition.return_value = (330, 573)

        namePosition: OglPosition = oglInterface._determineInterfaceNamePosition(mockDestinationAnchor, pixelSize=pixelSize, textSize=textSize)

        self.assertIsNotNone(namePosition, 'Minimally return an object')
        self.assertEqual(193, namePosition.x, 'West name position X is bad')
        self.assertEqual(549, namePosition.y, 'West name position Y is bad')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglInterface2))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
