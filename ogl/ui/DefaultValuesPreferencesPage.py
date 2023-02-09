from typing import List

from wx import BK_DEFAULT
from wx import Bitmap
from wx import ID_ANY
from wx import ImageList
from wx import Toolbook
from wx import Window

from wx.lib.embeddedimage import PyEmbeddedImage

# from pyut.dialogs.preferencesv2.valuecontrols.DefaultNamesControl import DefaultNamesControl
# from pyut.dialogs.preferencesv2.valuecontrols.NoteAttributesControl import NoteAttributesControl
# from pyut.dialogs.preferencesv2.valuecontrols.TextAttributesControl import TextAttributesControl
#
from hasiicommon.resources.images.DefaultPreferences import embeddedImage as DefaultPreferences

from hasiicommon.resources.images.icons.embedded16.ImgToolboxNote import embeddedImage as ImgToolboxNote
from hasiicommon.resources.images.icons.embedded16.ImgToolboxText import embeddedImage as ImgToolboxText
from hasiicommon.resources.images.icons.embedded16.ImgToolboxClass import embeddedImage as ImgToolboxClass
from wx.lib.sized_controls import SizedPanel

from ogl.ui.BaseOglPreferencesPage import BaseOglPreferencesPage
from ogl.ui.valuecontrols.ClassControl import ClassControl


def getNextImageID(count):
    imID = 0
    while True:
        yield imID
        imID += 1
        if imID == count:
            imID = 0


class DefaultValuesPreferencesPage(BaseOglPreferencesPage):

    def __init__(self, parent: Window):
        super().__init__(parent)
        self._layoutWindow(self)
        self._fixPanelSize(self)

    @property
    def name(self) -> str:
        return 'Default Values'

    def _layoutWindow(self, parent: SizedPanel):

        toolBook: Toolbook = Toolbook(parent, ID_ANY, style=BK_DEFAULT)
        toolBook.SetSizerProps(expand=True, proportion=1)

        embeddedImages: List[PyEmbeddedImage] = [ImgToolboxNote, ImgToolboxText, ImgToolboxClass, DefaultPreferences]
        imageList:      ImageList             = ImageList(width=16, height=16)

        for embeddedImage in embeddedImages:
            bmp: Bitmap = embeddedImage.GetBitmap()
            imageList.Add(bmp)

        toolBook.AssignImageList(imageList)

        imageIdGenerator = getNextImageID(imageList.GetImageCount())

        # notePanel:  NoteAttributesControl   = NoteAttributesControl(parent=toolBook)
        # textPanel:  TextAttributesControl   = TextAttributesControl(parent=toolBook)
        classPanel: ClassControl            = ClassControl(parent=toolBook)

        # defaultNamesPanel: DefaultNamesControl      = DefaultNamesControl(parent=toolBook)

        # toolBook.AddPage(notePanel,         text='Notes', select=True,  imageId=next(imageIdGenerator))
        # toolBook.AddPage(textPanel,         text='Text',  select=False, imageId=next(imageIdGenerator))
        toolBook.AddPage(classPanel,        text='Class', select=False, imageId=next(imageIdGenerator))
        # toolBook.AddPage(defaultNamesPanel, text='Names', select=False, imageId=next(imageIdGenerator))

    def _setControlValues(self):
        pass
