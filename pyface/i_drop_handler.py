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
""" This module defined a common interface for drag-drop handlers.

WIP; API may change without warning.

"""

from traits.api import Interface, Instance, Any


class IDragEvent(Interface):
	""" An event object for dragDrop events """

	data = Instance('pyface.mimedata:PyMimedata')

	target = Any('the drop target set on the widget, if any')

	source = Any('the source widget of the drop event')

	widget = Any('the widget on which the drop handler was set')

	def accept(self, action=None):
		""" Accept the event with the specified action.

		Action can be one of: copy, move or link; to perform the specified
		action on the dropped data.

		"""



class IDropHandler(Interface):
	""" Interface for a drop event handler

	This provides a uniform API to handle drop events on arbitrary widget.

	The basic usage is to implement the can_drop_handler() method and return
	True if the drop event can be handled, and do the appropriate action
	in the handle_drop() method. The can_handle_drop() method should not
	do any action which should happen on drop but only indicate that the
	drop can be handled.

	"""

	def can_handle_drop(self, event):
		""" Returns True if the drop handler can handle the given drag event.

		Parameters:
		-----------
		event - the `drop_handler:DragEvent` instance associated with the event

		Returns:
		--------
		bool - whether the event can be handled by this drop handler

		"""

	def handle_drop(self, event):
		""" Performs drop action when drop event occurs on target widget.

		Parameters:
		-----------
		event - the `drop_handler:DragEvent` instance associated with the event

		"""
