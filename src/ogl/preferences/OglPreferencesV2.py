
from logging import Logger
from logging import getLogger

from codeallybasic.SingletonV3 import SingletonV3


class OglPreferencesV2(metaclass=SingletonV3):

    def __init__(self):
        self._logger: Logger = getLogger(__name__)
