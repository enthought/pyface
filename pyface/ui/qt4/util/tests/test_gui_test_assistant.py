import unittest

from pyface.ui.qt4.util.gui_test_assistant import \
    GuiTestAssistant
from traits.api import Event, HasStrictTraits


class ExampleObject(HasStrictTraits):
    """ Test class; target for test_event_loop_until_traits_change. """
    spam = Event
    eggs = Event


class TestGuiTestAssistant(GuiTestAssistant, unittest.TestCase):
    def test_event_loop_until_traits_change_with_single_trait_success(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()

        # Successful case.
        with self.event_loop_until_traits_change(obj, 'spam'):
            obj.spam = True

    def test_event_loop_until_traits_change_with_single_trait_failure(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()

        # Failing case.
        with self.assertRaises(AssertionError):
            with self.event_loop_until_traits_change(obj, 'spam',
                                                     timeout=0.1):
                obj.eggs = True

    def test_event_loop_until_traits_change_with_multiple_traits_success(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()
        with self.event_loop_until_traits_change(obj, 'spam', 'eggs'):
            obj.spam = True
            obj.eggs = True

    def test_event_loop_until_traits_change_with_multiple_traits_failure(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()
        with self.assertRaises(AssertionError):
            with self.event_loop_until_traits_change(obj, 'spam', 'eggs',
                                                     timeout=0.1):
                obj.eggs = True

        # event_loop_until_traits_change calls self.fail on timeout.
        with self.assertRaises(AssertionError):
            with self.event_loop_until_traits_change(obj, 'spam', 'eggs',
                                                     timeout=0.1):
                obj.spam = True

    def test_event_loop_until_traits_change_with_no_traits_success(self):
        # event_loop_until_traits_change calls self.fail on timeout.
        obj = ExampleObject()

        # Successful case.
        with self.event_loop_until_traits_change(obj):
            pass
