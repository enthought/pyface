# Copyright (c) 2013 by Enthought, Inc., Austin, TX
# All rights reserved.
# This file is confidential and NOT open source.  Do not distribute.
""" Tools for testing. """


from contextlib import contextmanager

from pyface.qt.QtCore import QTimer
from pyface.util.guisupport import get_app_qt4


@contextmanager
def event_loop():
    """ Post and process the Qt events at the exit of the code block. """

    app = get_app_qt4()

    yield

    app.sendPostedEvents()
    app.processEvents()


@contextmanager
def delete_widget(widget, timeout=1.0):
    """ Context manager that executes the event loop so that we can safely
    delete a Qt widget.
    """

    app = get_app_qt4()

    timer = QTimer()
    timer.setSingleShot(True)
    timer.setInterval(timeout*1000)
    timer.timeout.connect(app.quit)
    widget.destroyed.connect(app.quit)

    yield

    timer.start()
    app.exec_()

    if not timer.isActive():
        # We exited the event loop on timeout.
        msg = 'Could not destroy widget before timeout: {!r}'
        raise AssertionError(msg.format(widget))
