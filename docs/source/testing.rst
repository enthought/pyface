.. _testing:

===========
GUI Testing
===========

GUI testing involves a slew of difficulties on top of what is normally
encountered when writing typical unit tests. The cause of this is having to
deal with the underlying event loop that drives the GUI. Consider a scenario
in which you have a simple :class:`~traits.has_traits.HasTraits` class and you call
:meth:`~traits.has_traits.HasTraits.configure_traits` on it to start the application. Typically python
execution stops at this point and control is passed to the underlying toolkit
event loop. In a test context though, we need access to that event loop inside
the test. To simulate and test GUI interactions, we need to be able to post
events to the event loop, process them manually, and then make assertions about
the desired behavior. Even further, the event loop is global state, and so
great care needs to be taken in each test to pick up after itself to avoid
interactions with other tests. This is still necessary even if the test fails. 

Pyface provides a few utilities that are useful in this process.  Namely,
:class:`~pyface.util.GuiTestAssistant` and
:class:`~pyface.util.ModalDialogTester`.


GuiTestAssistant
================

.. note::

   GuiTestAssistant is currently only available on Qt.

:class:`GuiTestAssistant` is a mixin class intended to to augment
:class:`python:unittest.TestCase`. In fact, it has
:class:`~traits.testing.unittest_tools.UnittestTools` from traits as a base
class and thus gives access to methods like
:meth:`~traits.testing.unittest_tools.UnittestTools.assertTraitChanges`. See the
`Traits Testing documentation <https://docs.enthought.com/traits/traits_user_manual/testing.html#testing>`_
for more. 

:class:`GuiTestAssistant` holds a reference to a :class:`pyface.gui.GUI` object
(for api details see the interface :class:`~pyface.i_gui.IGUI`) which is what
gives the low level access to the event loop. `pyface.GUI` provides methods such as
:meth:`~pyface.i_gui.IGUI.start_event_loop`,
:meth:`~pyface.i_gui.IGUI.stop_event_loop`,
:meth:`~pyface.i_gui.IGUI.process_events`,
:meth:`~pyface.i_gui.IGUI.invoke_later`, and
:meth:`~pyface.i_gui.IGUI.set_trait_later`. This is accessible via the
:attr:`gui` attribute on :class:`GuiTestAssistant`.

What :class:`GuiTestAssistant` provides that is novel, is effectively more
security to make sure your tests clean up after themselves.  For example,
:class:`GuiTestAssistant` provides standard :meth:`setUp` and :meth:`tearDown`
methods which try to clean up existing UI state and empty the event loop even
if a test fails.  In addition, the methods typically have timouts so that the
test will fail rather than blocking forever in the case something has gone
wrong. Effectively, the class aims to remember to do the overhead to ensure
your tests don't cause trouble, and at the same time give you the low level
event loop access needed to write your GUI tests.


This class provides the following methods (some of them being context managers):

- :meth:`event_loop`
  
    Takes an integer ``repeat`` parameter and artificially replicates the event
    loop by Calling :meth:`sendPostedEvents` and :meth:`processEvents` ``repeat``
    number of times.

- :meth:`event_loop_until_condition`

    Runs the real Qt event loop until the provided condition evaluates to True.

- :meth:`event_loop_until_traits_change`

    Run the real application event loop until a change notification for all of
    the specified traits is received.

- :meth:`event_loop_with_timeout`

    Helper context manager to send all posted events to the event queue
    and wait for them to be processed.

    This differs from the `event_loop()` context manager in that it
    starts the real event loop rather than emulating it with
    ``QApplication.processEvents()``

- :meth:`find_qt_widget`

    Takes parameters ``start``, ``type_`` and ``test``. Recursively walks the Qt
    widget tree from Qt widget ``start`` until it finds a widget of type ``type_``
    (a QWidget subclass) that satisfies the provided ``test`` method.

- :meth:`delete_widget`

    Runs the real Qt event loop until the widget provided has been
    deleted.

- :meth:`assertEventuallyTrueInGui` 

    Assert that the given condition becomes true if we run the GUI
    event loop for long enough.

    This assertion runs the real Qt event loop, polling the condition
    and returning as soon as the condition becomes true. If the condition
    does not become true within the given timeout, the assertion fails.

- :meth:`assertTraitChangesInEventLoop`

    Runs the real Qt event loop, collecting trait change events until
    the provided condition evaluates to True.

.. TODO: Add example test code

ModalDialogTester
=================

.. note::

   ModalDialogTester is currently only available on Qt.

:class:`ModalDialogTester` is, as the name suggests, intended specifically for
use testing modal dialogs. Modal dialogs are dialogs which sit on top of the 
main content of the application, and effectively demand interaction.  The
rest of the UI is blocked until the dialog is addressed. These require special
care to test and :class:`GuiTestAssistant` doesen't provide this functionality.
When testing modal dialog related code the main recommendation for doing so is
try to avoid it. If you can, try testing the dialog in a non-modal fashion. Or,
if possible for your use case, use :mod:`python:unittest.mock` to patch the
class or its "open" method with a dummy implementation that returns a useful
result. If you absolutely do need to test the real modal dialog in a modal
fashion, :class:`ModalDialogTester` aims to help make this as easy as possible.

To use it, instantiate a :class:`ModalDialogTester` instance, passing it a
function taking 0 arguments which when called opens the modal dialog. From
there you can call the :meth:`open_and_run` method on the tester object just
instantiated, and pass in a ``when_opened`` callable which will take the tester
object as its sole argument. This method first calls the function to open the
dialog and then subsequently the ``when_opened`` callable.  In the body of the
``when_opened`` callable is where you define the interactions with the modal
dialog you want to be performed during the test. You can use the
:meth:`get_dialog_widget` method on the tester object (accesible since this is
passed as an argument to ``when_opened``) to get access to the UI for the
dialog. Then interactions can be performed using methods such as
:meth:`find_qt_widget`, :meth:`click_widget`, etc. Alternatively, if working
with a TraitsUI applicatino, you could use the TraitsUI
:class:`~traitsui.testing.tester.ui_tester.UITester` to perform these interactions (see the
`TraitsUI Testing documentation <https://docs.enthought.com/traitsui/traitsui_user_manual/testing.html>`_).
To verify the dailog was indeed opened once, you can run
``self.assertTrue(tester.dialog_was_opened)``.

Additionally, :class:`ModalDialogTester` provides a context manager
:meth:`capture_error` to be used inside te event loop. When errors or failures
occur they could be missed by :mod:`python:unittest`, but this catches them.
These can then be checked with the :meth:`assert_no_errors_collected` method.

For a very simple example consider this (slightly modified) test from pyface's
own test suite.

::

    import unittest

    from pyface.api import Dialog, OK
    from pyface.util.modal_dialog_tester import ModalDialogTester

    class TestDialog(unittest.TestCase):

        def test_accept(self):
            dialog = Dialog()
            # test that accept works as expected
            tester = ModalDialogTester(dialog.open)
            tester.open_and_run(when_opened=lambda x: x.close(accept=True))

            self.assertTrue(tester.dialog_was_opened)
            self.assertEqual(tester.result, OK)
            self.assertEqual(dialog.return_code, OK)
