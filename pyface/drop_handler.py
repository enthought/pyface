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
WIP, interface may change without warnings.

Usage:
------
On any toolkit widget on which you wish to handle drops, call the function::

    add_drop_handler(widget, handler)

with the handler being an instance of BaseDropHandler.

If you need to pass additional python object to the handler's event,
you can do it by calling the method:

    set_drop_target(widget, target)

with the target being an object which is set as the DropEvent's target
attribute and can be used by drop handlers to perform any actions they need.

"""

# Enthought library imports
from pyface.toolkit import toolkit_object
from pyface.i_drop_handler import IDropHandler
from pyface.mimedata import PyMimeData
from traits.api import HasTraits, Callable, implements, List, Str


class DragEvent(object):
    """ The event class for drag-drop events.

    Attributes:
    -----------
    data - The instance of PyMimeData associated with the drag event
    widget - The widget (toolkit widget) on which the drop handler was set
    target - The drop target set on the widget, if any
    source - The source widget for the event

    Notes:
    ------
    Most likely you will only use the data and the target attributes,
    since others will not be toolkit-portable.

    """
    def __init__(self, data, widget, target, source, native_event=None):
        self.data = data
        self.target = target
        self.widget = widget
        self.source = source
        self._event = native_event
        self._action = None

    def accept(self, action=True):
        self._action = action



class BaseDropHandler(HasTraits):
    """ Basic drop handler
    """
    implements(IDropHandler)

    ### BaseDropHandler interface #############################################

    # Returns True if the current drop handler can handle the given drag event
    # occurring on the given target widget.
    # The argument to callable is the DragEvent
    on_can_handle = Callable

    # Performs drop action when drop event occurs on target widget.
    # The argument to callable is the DragEvent
    on_handle = Callable

    ### IDropHandler interface ################################################

    def can_handle_drop(self, event):
        return self.on_can_handle(event)

    def handle_drop(self, event):
        return self.on_handle(event)


class FileDropHandler(BaseDropHandler):
    """ Class to handle file drops.
    """
    implements(IDropHandler)

    ### FileDropHandler interface #############################################

    # supported extensions
    extensions = List(Str)

    # Called when file is opened. Takes single argument: path of file
    open_file = Callable

    ### IDropHandler interface ################################################

    def can_handle_drop(self, event):
        for file_path in event.data.local_paths():
            if file_path.endswith(tuple(self.extensions)):
                return True
        return False

    def handle_drop(self, event):
        if not self.can_handle_drop(event):
            return False

        accepted = False
        for file_path in event.data.local_paths():
            self.open_file(file_path)
            accepted = True
        return accepted


# Add a drop handler to the toolkit widget.
add_drop_handler = toolkit_object('drop_handler:add_drop_handler')

# Set the drop event's target to the specified object.
# This must be called only once for a widget, multiple invocations
# replace the previous target.
set_drop_target = toolkit_object('drop_handler:set_drop_target')

