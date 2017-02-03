# Dummy widget module for testing entrypoints

from traits.api import provides
from pyface.i_widget import IWidget, MWidget


@provides(IWidget)
class Widget(MWidget):
    pass
