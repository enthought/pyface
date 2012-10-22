from traits.api import Interface, HasTraits, Callable, implements

class IDropHandler(Interface):
	""" Interface for a drop event handler, which provides API to check if the drop can
	be handled or not, and then handle it if possible.
	"""

	# Returns True if the current drop handler can handle the given drag event 
	# occurring on the given target widget.
	can_handle_drop = Callable

	# Performs drop action when drop event occurs on target widget. Returns True 
	# if it successfully handled the event, otherwise False. Does nothing if it 
	# couldn't handle the event.
	handle_drop = Callable

class BaseDropHandler(HasTraits):
	""" Basic drop handler
	"""
	implements(IDropHandler)

	# Returns True if the current drop handler can handle the given drag event 
	# occurring on the given target widget.
	can_handle_drop = Callable

	# Performs drop action when drop event occurs on target widget. Returns True 
	# if it successfully handled the event, otherwise False. Does nothing if it 
	# couldn't handle the event.
	handle_drop = Callable

	def _can_handle_drop_default(self):
		return self._can_handle_drop

	def _handle_drop_default(self):
		return self._handle_drop

	### Private interface #####################################################

	def _can_handle_drop(self, event, target):
		return False

	def _handle_drop(self, event, target):
		return False