
from typing import NewType
from typing import List

from logging import Logger
from logging import getLogger


class OglSDMessageV2():

    def __init__(self):
        self.logger: Logger = getLogger(__name__)


OglSDMessages = NewType("OglSDMessages", List[OglSDMessageV2])