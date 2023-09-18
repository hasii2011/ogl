
from unittest import TestSuite
from unittest import main as unitTestMain

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW

from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage


class TestOglSDMessage(UnitTestBaseW):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def testBasicCreation(self):

        srcPyutSDInstance: PyutSDInstance = PyutSDInstance()
        srcSDInstance:  OglSDInstance  = OglSDInstance(pyutObject=srcPyutSDInstance)

        dstPyutSDInstance: PyutSDInstance = PyutSDInstance()
        dstSDInstance:  OglSDInstance  = OglSDInstance(pyutObject=dstPyutSDInstance)

        pyutSDMessage: PyutSDMessage = PyutSDMessage()
        sdMessage:     OglSDMessage  = OglSDMessage(srcSDInstance=srcSDInstance, dstSDInstance=dstSDInstance, pyutSDMessage=pyutSDMessage)

        self.assertIn(sdMessage, srcSDInstance.links, 'Message not in source Ogl instance')
        self.assertIn(sdMessage, dstSDInstance.links, 'Message not in destination Ogl instance')


def suite() -> TestSuite:

    import unittest

    testSuite: TestSuite = TestSuite()

    testSuite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(testCaseClass=TestOglSDMessage))

    return testSuite


if __name__ == '__main__':
    unitTestMain()
