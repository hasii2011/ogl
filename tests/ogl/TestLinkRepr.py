
from typing import cast

from dataclasses import dataclass

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutLink import PyutLink
from pyutmodel.PyutLinkType import PyutLinkType

from ogl.OglAggregation import OglAggregation
from ogl.OglAssociation import OglAssociation
from ogl.OglClass import OglClass
from ogl.OglComposition import OglComposition
from ogl.OglInterface import OglInterface
from tests.TestBase import TestBase


SOURCE_CLASS_NAME:      str = 'SourceClass'
DESTINATION_CLASS_NAME: str = 'DestinationClass'

SOURCE_PYUT_CLASS_ID:      int = 1000
DESTINATION_PYUT_CLASS_ID: int = 2000

SOURCE_OGL_CLASS_ID:      int = 5555
DESTINATION_OGL_CLASS_ID: int = 6666


@dataclass
class LinkClasses:
    srcOglClass: OglClass = cast(OglClass, None)
    dstOglClass: OglClass = cast(OglClass, None)
    pyutLink:    PyutLink = cast(PyutLink, None)


class TestLinkRepr(TestBase):
    """
    This test class test multiple classes that subclass OglLink.  Usually,
    I have one test class per "tested" class.  However, since I am testing
    a single inherited method with lots of common code, I felt good about
    combining them here
    """

    def setUp(self):
        super().setUp()
        self._linkClasses: LinkClasses = self._createLinkClasses()

    def tearDown(self):
        pass

    def testOglInterfaceRepr(self):

        oglInterface: OglInterface = OglInterface(srcShape=self._linkClasses.srcOglClass,
                                                  pyutLink=self._linkClasses.pyutLink,
                                                  dstShape=self._linkClasses.dstOglClass)
        expectedRepr: str = self._createdExpectedReprString('OglInterface')
        actualRepr:   str = oglInterface.__repr__()

        self.assertEqual(expectedRepr, actualRepr, 'Debug aid has changed')

    def testOglAssociationRepr(self):

        oglAssociation: OglAssociation = OglAssociation(srcShape=self._linkClasses.srcOglClass,
                                                        pyutLink=self._linkClasses.pyutLink,
                                                        dstShape=self._linkClasses.dstOglClass)

        expectedRepr: str = self._createdExpectedReprString('OglAssociation')
        actualRepr:   str = oglAssociation.__repr__()

        self.assertEqual(expectedRepr, actualRepr, 'Debug aid has changed')

    def testOglCompositionRepr(self):

        oglComposition: OglComposition = OglComposition(srcShape=self._linkClasses.srcOglClass,
                                                        pyutLink=self._linkClasses.pyutLink,
                                                        dstShape=self._linkClasses.dstOglClass)

        expectedRepr: str = self._createdExpectedReprString('OglComposition')
        actualRepr:   str = oglComposition.__repr__()

        self.assertEqual(expectedRepr, actualRepr, 'Debug aid has changed')

    def testOglAggregationRepr(self):

        oglAggregation: OglAggregation = OglAggregation(srcShape=self._linkClasses.srcOglClass,
                                                        pyutLink=self._linkClasses.pyutLink,
                                                        dstShape=self._linkClasses.dstOglClass)

        expectedRepr: str = self._createdExpectedReprString('OglAggregation')
        actualRepr:   str = oglAggregation.__repr__()

        self.assertEqual(expectedRepr, actualRepr, 'Debug aid has changed')

    def _createLinkClasses(self) -> LinkClasses:

        srcPyutClass: PyutClass = PyutClass(name=SOURCE_CLASS_NAME)
        dstPyutClass: PyutClass = PyutClass(name=DESTINATION_CLASS_NAME)

        srcPyutClass.id = SOURCE_PYUT_CLASS_ID       # Picked so when executed with TestAll we do not
        dstPyutClass.id = DESTINATION_PYUT_CLASS_ID  # Get some random one

        srcClass: OglClass = OglClass(pyutClass=srcPyutClass)
        dstClass: OglClass = OglClass(pyutClass=dstPyutClass)

        srcClass.id = SOURCE_OGL_CLASS_ID
        dstClass.id = DESTINATION_OGL_CLASS_ID
        pyutLink: PyutLink = PyutLink(linkType=PyutLinkType.INTERFACE, source=srcPyutClass, destination=dstPyutClass)

        linkClasses: LinkClasses = LinkClasses()
        linkClasses.srcOglClass = srcClass
        linkClasses.dstOglClass = dstClass
        linkClasses.pyutLink    = pyutLink

        return linkClasses

    def _createdExpectedReprString(self, linkClassName: str) -> str:

        # - from: id: 5555 OglClass.SourceClass modelId: 1000 to: id: 6666 OglClass.DestinationClass modelId: 2000
        expectedRepr: str = (
            f'{linkClassName} - from: '
            f'id: {SOURCE_OGL_CLASS_ID} '
            f'OglClass.SourceClass modelId: {SOURCE_PYUT_CLASS_ID} '
            f'to '
            f'id: {DESTINATION_OGL_CLASS_ID} '
            f'OglClass.DestinationClass modelId: {DESTINATION_PYUT_CLASS_ID}'
        )
        return expectedRepr


def suite() -> TestSuite:
    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestLinkRepr))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
