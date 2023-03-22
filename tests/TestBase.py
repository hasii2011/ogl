
import json

import logging
import logging.config

from unittest import TestCase

from importlib.abc import Traversable
from importlib.resources import files

from wx import App
from wx import Frame
from wx import ID_ANY

from miniogl.DiagramFrame import DiagramFrame

JSON_LOGGING_CONFIG_FILENAME: str = "testLoggingConfig.json"
TEST_DIRECTORY:               str = 'tests'


class DummyApp(App):
    def OnInit(self):
        return True


class TestBase(TestCase):

    RESOURCES_PACKAGE_NAME:                   str = 'tests.resources'
    RESOURCES_TEST_CLASSES_PACKAGE_NAME:      str = 'tests.resources.testclass'
    RESOURCES_TEST_JAVA_CLASSES_PACKAGE_NAME: str = 'tests.resources.testclass.ozzee'
    RESOURCES_TEST_DATA_PACKAGE_NAME:         str = 'tests.resources.testdata'
    RESOURCES_TEST_IMAGES_PACKAGE_NAME:       str = 'tests.resources.testimages'

    def setUp(self):
        self._app:   DummyApp = DummyApp()

        #  Create frame
        baseFrame: Frame = Frame(None, ID_ANY, "", size=(10, 10))
        # noinspection PyTypeChecker
        umlFrame = DiagramFrame(baseFrame)
        umlFrame.Show(True)

    def tearDown(self):
        self._app.OnExit()

    """
    A base unit test class to initialize some logging stuff we need
    """
    @classmethod
    def setUpLogging(cls):
        """"""

        loggingConfigFilename: str = cls.getLoggingConfigurationFileName()

        with open(loggingConfigFilename, 'r') as loggingConfigurationFile:
            configurationDictionary = json.load(loggingConfigurationFile)

        logging.config.dictConfig(configurationDictionary)
        logging.logProcesses = False
        logging.logThreads = False

    @classmethod
    def getLoggingConfigurationFileName(cls) -> str:

        fqFileName: str = cls.getFullyQualifiedResourceFileName(TestBase.RESOURCES_PACKAGE_NAME, fileName=JSON_LOGGING_CONFIG_FILENAME)
        return fqFileName

    @classmethod
    def getFullyQualifiedResourceFileName(cls, package: str, fileName: str) -> str:

        traversable: Traversable = files(package) / fileName

        return str(traversable)
