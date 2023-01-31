
from typing import cast

from logging import Logger
from logging import getLogger

from unittest import TestSuite
from unittest import main as unitTestMain

from pyutmodel.PyutSDInstance import PyutSDInstance
from pyutmodel.PyutSDMessage import PyutSDMessage

from tests.TestBase import TestBase

from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage


class TestOglSDMessage(TestBase):
    """
    """
    clsLogger: Logger = cast(Logger, None)

    @classmethod
    def setUpClass(cls):
        TestBase.setUpLogging()
        TestOglSDMessage.clsLogger = getLogger(__name__)

    def setUp(self):
        self.logger: Logger = TestOglSDMessage.clsLogger
        super().setUp()

    def tearDown(self):
        pass

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
    """You need to change the name of the test class here also."""
    import unittest

    testSuite: TestSuite = TestSuite()
    # noinspection PyUnresolvedReferences
    testSuite.addTest(unittest.makeSuite(TestOglSDMessage))

    return testSuite


if __name__ == '__main__':
    unitTestMain()