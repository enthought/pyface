# System library imports.
from pyface.qt import QtCore

###############################################################################
# Functions.
###############################################################################

def set_focus(control):
    """ Assign keyboard focus to the given control.

    Ideally, we would just call ``setFocus()`` on the control and let Qt do the
    right thing. Unfortunately, this method is implemented in the most naive
    manner possible, and is essentially a no-op if the toplevel widget does not
    itself accept focus. We adopt the following procedure:

    1. If the control itself accepts focus, use it. This is important since the
       control may have custom focus dispatching logic.
       
    2. Otherwise, if there is a child widget of the control that previously had
       focus, use it.
       
    3. Finally, have Qt determine the next item using its internal logic. Qt
       will only restrict itself to this widget's children if it is a Qt::Window
       or Qt::SubWindow, hence the hack below.
    """
    if control.focusPolicy() != QtCore.Qt.NoFocus:
        control.setFocus()
    else:
        widget = control.focusWidget()
        if widget:
            widget.setFocus()
        else:
            flags = control.windowFlags()
            control.setWindowFlags(flags | QtCore.Qt.SubWindow)
            try:
                control.focusNextChild()
            finally:
                control.setWindowFlags(flags)
