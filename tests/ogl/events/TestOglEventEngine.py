
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from tests.miniogl.TestMiniOglCommon import Point

from pyutmodelv2.PyutClass import PyutClass

from miniogl.AttachmentSide import AttachmentSide
from miniogl.SelectAnchorPoint import SelectAnchorPoint

from ogl.OglClass import OglClass

from ogl.events.OglEventEngine import OglEventEngine
from ogl.events.OglEvents import OglEventType
from ogl.events.InvalidKeywordException import InvalidKeywordException


class TestOglEventEngine(UnitTestBaseW):
    """
    This unit test mainly verifies that improperly using an incorrect kwargs keyword
    appropriately fails
    """

    def setUp(self):
        super().setUp()
        self._eventEngine: OglEventEngine = OglEventEngine(listeningWindow=self._listeningWindow)

    def tearDown(self):
        super().tearDown()

    def testIncorrectShapeToCutEventKeyword(self):

        pyutClass: PyutClass = PyutClass(name='OglTestClass')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)

        self.assertRaises(InvalidKeywordException, lambda: self._eventEngine.sendEvent(OglEventType.CutOglClass, shapeToCutBAD=oglClass))

    def testIncorrectRequestLollipopLocation(self):
        """
        """

        pyutClass: PyutClass = PyutClass(name='ClassRequestingLollipopLocation')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.RequestLollipopLocation, requestShapeBAD=oglClass))

    def testIncorrectSelectedShapeKeywordShape(self):

        pyutClass: PyutClass = PyutClass(name='TestShape')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.ShapeSelected, shapeBAD=oglClass, position=Point(100, 100)))

    def testIncorrectSelectedShapeKeywordPosition(self):
        pyutClass: PyutClass = PyutClass(name='TestShape')
        oglClass:  OglClass  = OglClass(pyutClass=pyutClass)
        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.ShapeSelected, shape=oglClass, positionBad=Point(100, 100)))

    def testIncorrectCreateLollipopInterfaceKeywordImplementor(self):
        pyutClass:       PyutClass         = PyutClass(name='Implementor')
        implementor:     OglClass          = OglClass(pyutClass=pyutClass)
        attachmentPoint: SelectAnchorPoint = SelectAnchorPoint(x=100, y=100, attachmentSide=AttachmentSide.SOUTH, parent=implementor)

        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.CreateLollipopInterface, implementorBAD=implementor,
                                                              attachmentPoint=attachmentPoint))

    def testIncorrectCreateLollipopInterfaceKeywordAttachmentPoint(self):
        pyutClass:       PyutClass         = PyutClass(name='Implementor')
        implementor:     OglClass          = OglClass(pyutClass=pyutClass)
        attachmentPoint: SelectAnchorPoint = SelectAnchorPoint(x=100, y=100, attachmentSide=AttachmentSide.SOUTH, parent=implementor)

        self.assertRaises(InvalidKeywordException,
                          lambda: self._eventEngine.sendEvent(OglEventType.CreateLollipopInterface, implementor=implementor,
                                                              attachmentPointBAD=attachmentPoint))


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglEventEngine))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
