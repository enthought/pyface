#------------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" Module to handle drag-drop on widgets.
Work-in-progress, interface may change without warnings. """

from pyface.qt import QtCore
from pyface.drop_handler import DragEvent, BaseDropHandler
from pyface.mimedata import PyMimeData


drop_action_map = {'copy':QtCore.Qt.CopyAction,
                   'move':QtCore.Qt.MoveAction,
                   'link':QtCore.Qt.LinkAction,
                   None:QtCore.Qt.IgnoreAction}

inv_drop_action_map = {value:key for key,value in drop_action_map.items()}


class _DropEventEmitter(QtCore.QObject):
    def __init__(self, widget):
        QtCore.QObject.__init__(self, widget)
        self.target = None
        self.widget = widget

        widget.setAcceptDrops(True)
        widget.installEventFilter(self)

        self._drop_evt = None

        self._handlers = []

    def eventFilter(self, source, event):
        """ Handle drop events on widget. """
        typ = event.type()
        if typ == QtCore.QEvent.DragEnter:
            self._handler = self._drop_evt = None
            data = PyMimeData.coerce(event.mimeData())
            evt = DragEvent(data=data, target=self.target,
                            widget=self.widget, source=source,
                            native_event=event)
            for handler in self._handlers:
                if handler.can_handle_drop(evt):
                    self._drop_evt = evt
                    self._handler = handler
                    if evt._action is None:
                        event.acceptProposedAction()
                    else:
                        event.setDropAction(drop_action_map[evt._action])
                        event.accept()
                    return True
            return False

        elif typ == QtCore.QEvent.Drop:
            evt = self._drop_evt
            if evt is None:
                return False
            try:
                evt.source = source
                evt._event = event
                self._handler.handle_drop(evt)
                event.acceptProposedAction()
            finally:
                self._handler = self._drop_evt = None
                return True

        elif typ == QtCore.QEvent.DragLeave:
            self._handler = self._drop_evt = None

        return QtCore.QObject.eventFilter(self, source, event)

    def add_handler(self, handler):
        self._handlers.append(handler)


def _get_emitter_for_widget(widget):
    emitter = widget.findChild(_DropEventEmitter)
    if emitter is None:
        emitter = _DropEventEmitter(widget)
    return emitter


def set_drop_target(widget, target):
    """ Sets the drop target for the given widget. """
    emitter = _get_emitter_for_widget(widget)
    emitter.target = target


def add_drop_handler(widget, drop_handler):
    """ Add drop handler to widget.

    Parameters
    ----------
    widget - The widget on which drop events are listened for.
    handler - The drop handler to add.

    """
    emitter = _get_emitter_for_widget(widget)
    emitter.add_handler(drop_handler)


if __name__ == '__main__':
    from pyface.qt import QtGui
    app = QtGui.QApplication.instance() or QtGui.QApplication([])

    text_ctrl = QtGui.QTextBrowser()
    text_ctrl.setText('Drop anything here')
    text_ctrl.setMinimumSize(300, 300)

    def can_handle_drop(evt):
        print 'can_drop'
        return True

    def handle_drop(evt):
        print 'drop', evt.data.formats()
        text = u''
        for format in evt.data.formats():
            try:
                text += u'format: %s:\n%s\n\n'%(format, evt.data.data(format))
            except UnicodeDecodeError:
                text += u'format: %s: %s bytes\n\n'%(format, len(evt.data.data(format)))
        text_ctrl.setText(text)

    add_drop_handler(text_ctrl, BaseDropHandler(on_can_handle=can_handle_drop,
                                                on_handle=handle_drop))

    text_ctrl.show()
    app.exec_()

