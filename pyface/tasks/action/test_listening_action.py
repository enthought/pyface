import unittest
from listening_action import ListeningAction
from traits.api import HasTraits


class TestListeningAction(unittest.TestCase):

	def setUp(self):
		""" Creates a dummy class to apply listening action to
		"""
		class _DummyClass(HasTraits):
			""" Dummy class to apply ListeningAction to
			"""
			def __init__(self, enabled=False, visible=False):
				self.args = []
				self.kwargs = {}
				self.enabled = enabled
				self.visible = visible

			def dummy_method(self, *args, **kwargs):
				self.args.extend(args)
				self.kwargs.update(kwargs)
		self._class = _DummyClass
	
	def test_method(self):
		""" Tests whether the method attribute supports extra positional 
		and keyword arguments.
		"""
		# works with additional arguments?
		dummy_obj = self._class()
		action = ListeningAction(object=dummy_obj, method='dummy_method',
								args=['arg1', 'arg2'], 
								kwargs={'arg1_pos': 0, 'arg2_pos': 1})
		action.perform()
		self.assertEquals(dummy_obj.args, ['arg1', 'arg2'])
		self.assertEquals(dummy_obj.kwargs, {'arg1_pos': 0, 'arg2_pos': 1})

		# works without any argument?
		dummy_obj = self._class()
		action = ListeningAction(object=dummy_obj, method='dummy_method')
		action.perform()
		self.assertEquals(dummy_obj.args, [])
		self.assertEquals(dummy_obj.kwargs, {})

		# nothing happens if the specified method doesn't exist?
		dummy_obj = self._class()
		action = ListeningAction(object=dummy_obj, method='other_dummy_method')
		action.perform()
		self.assertEquals(dummy_obj.args, [])
		self.assertEquals(dummy_obj.kwargs, {})

	def test_enabled_name(self):
		""" Whether the action follows enabled_name attribute of object to 
		enable/disable the action
		"""
		# enabled by default since enabled_name is not specified
		dummy_obj = self._class()
		action = ListeningAction(object=dummy_obj)
		self.assertEquals(action.enabled, True)

		# disabled since the specified enabled_name attribute is set to False
		dummy_obj = self._class(enabled=False)
		action = ListeningAction(object=dummy_obj, enabled_name='enabled')
		self.assertEquals(action.enabled, False)

		# what if enabled_name attribute of object is changed
		dummy_obj.enabled = True
		self.assertEquals(action.enabled, True)

	def test_visible_name(self):
		""" Whether the action follows visible_name attribute of object to 
		make the action visible/invisible
		"""
		# enabled by default since enabled_name is not specified
		dummy_obj = self._class()
		action = ListeningAction(object=dummy_obj)
		self.assertEquals(action.visible, True)

		# disabled since the specified enabled_name attribute is set to False
		dummy_obj = self._class(visible=False)
		action = ListeningAction(object=dummy_obj, visible_name='visible')
		self.assertEquals(action.visible, False)

		# what if visible_name attribute of the object is changed
		dummy_obj.visible = True
		self.assertEquals(action.visible, True)


if __name__=="__main__":
	unittest.main()
