# Copyright (c) 2013 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Tools for testing. """

from __future__ import print_function
from contextlib import contextmanager
import os
import sys

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


@contextmanager
def _convert_none_to_null_handle(stream):
    """ If 'stream' is None, provide a temporary handle to /dev/null. """

    if stream is None:
        out = open(os.devnull, 'w')
        try:
            yield out
        finally:
            out.close()
    else:
        yield stream


@contextmanager
def silence_output(out=None, err=None):
    """ Re-direct the stderr and stdout streams while in the block. """

    with _convert_none_to_null_handle(out) as out:
        with _convert_none_to_null_handle(err) as err:
            _old_stderr = sys.stderr
            _old_stderr.flush()

            _old_stdout = sys.stdout
            _old_stdout.flush()

            try:
                sys.stdout = out
                sys.stderr = err
                yield
            finally:
                sys.stdout = _old_stdout
                sys.stderr = _old_stderr


def print_qt_widget_tree(widget, level=0):
    """ Debugging helper to print out the Qt widget tree starting at a
    particular `widget`.

    Parameters
    ----------
    widget : QObject
        The root widget in the tree to print.
    level : int
        The current level in the tree. Used internally for displaying the
        tree level.
    """
    level = level + 4
    if level == 0:
        print()
    print(' '*level, widget)
    for child in widget.children():
        print_qt_widget_tree(child, level=level)
    if level == 0:
        print()


def find_qt_widget(start, type_, test=None):
    """Recursively walks the Qt widget tree from Qt widget `start` until it
    finds a widget of type `type_` (a QWidget subclass) that
    satisfies the provided `test` method.

    Parameters
    ----------
    start : QWidget
        The widget from which to start walking the tree
    type_ : type
        A subclass of QWidget to use for an initial type filter while
        walking the tree
    test : callable
        A filter function that takes one argument (the current widget being
        evaluated) and returns either True or False to determine if the
        widget matches the required criteria.
    """
    if test is None:
        test = lambda widget: True
    if isinstance(start, type_):
        if test(start):
            return start
    for child in start.children():
        widget = find_qt_widget(child, type_, test=test)
        if widget:
            return widget
    return None
