

from codeallyadvanced.ui.UnitTestBaseW import UnitTestBaseW


class TestBase(UnitTestBaseW):
    """
    Use the UI version
    """
    RESOURCES_TEST_IMAGES_PACKAGE_NAME: str = 'tests.resources.testimages'

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
