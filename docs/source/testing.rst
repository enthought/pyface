.. _testing:

===========
GUI Testing
===========

GUI testing involves a slew of difficulties on top of what is normally
encountered when writing typical unit tests. This is a result of having to deal
with the underlying event loop that drives the GUI. Consider a scenario in
which you have a simple :class:`~traits.has_traits.HasTraits` class and you call
:meth:`~traits.has_traits.HasTraits.configure_traits` on it to start the
application. Typically python execution stops at this point and control is
passed to the underlying event loop. In a test context though, we need
direct access to that event loop. To simulate and test GUI interactions we need
to be able to post events to the event loop, process them manually, and then
make assertions about the desired behavior. Even further, the event loop is
global state. Therefore, great care needs to be taken in each test to pick up
after itself to avoid interactions with other tests. This is still necessary
even if the test fails.

Pyface provides a few utilities that are useful in this process.  Namely,
:class:`~pyface.util.GuiTestAssistant` and
:class:`~pyface.util.ModalDialogTester`.


GuiTestAssistant
================

.. note::

   GuiTestAssistant is currently only available on Qt.

:class:`GuiTestAssistant` is a mixin class intended to augment
:class:`python:unittest.TestCase`. In fact, it inherits from
:class:`~traits.testing.unittest_tools.UnittestTools` from Traits and thus
gives access to methods like
:meth:`~traits.testing.unittest_tools.UnittestTools.assertTraitChanges`. See the
`Traits Testing documentation <https://docs.enthought.com/traits/traits_user_manual/testing.html#testing>`_
for more.

:class:`GuiTestAssistant` holds a reference to a :class:`pyface.gui.GUI` object
(for api details see the interface :class:`~pyface.i_gui.IGUI`) which is what
gives the low level access to the event loop. :class:`pyface.gui.GUI` provides methods such as
:meth:`~pyface.i_gui.IGUI.start_event_loop`,
:meth:`~pyface.i_gui.IGUI.stop_event_loop`,
:meth:`~pyface.i_gui.IGUI.process_events`,
:meth:`~pyface.i_gui.IGUI.invoke_later`, and
:meth:`~pyface.i_gui.IGUI.set_trait_later`. This is accessible via the
:attr:`gui` attribute on :class:`GuiTestAssistant`.

What :class:`GuiTestAssistant` provides that is novel, is effectively better
control to ensure that your tests clean up after themselves.  For example,
:class:`GuiTestAssistant` provides standard :meth:`setUp` and :meth:`tearDown`
methods which try to clean up existing UI state and empty the event loop even
if a test fails.  In addition, the methods typically have timeouts so that the
test will fail rather than blocking forever in the case something has gone
wrong. Effectively, the class aims to remember to do the overhead to ensure
your tests don't cause trouble, and at the same time give you the low level
event loop access needed to write your GUI tests.


This class provides the following methods (some of them being context managers):

- :meth:`event_loop`

    Context Manager

    Takes an integer ``repeat`` parameter and artificially replicates the event
    loop by calling :meth:`sendPostedEvents` and :meth:`processEvents` ``repeat``
    number of times.

- :meth:`event_loop_until_condition`

    Context Manager

    Runs the real Qt event loop until the provided condition evaluates to True.

- :meth:`event_loop_until_traits_change`

    Context Manager

    Run the real application event loop until a change notification for all of
    the specified traits is received.

- :meth:`event_loop_with_timeout`

    Context Manager

    Helper context manager to send all posted events to the event queue
    and wait for them to be processed.

    This differs from the `event_loop()` context manager in that it
    starts the real event loop rather than emulating it with
    ``QApplication.processEvents()``

- :meth:`assertTraitChangesInEventLoop`

    Context Manager

    Runs the real Qt event loop, collecting trait change events until
    the provided condition evaluates to True.

- :meth:`delete_widget`

    Context Manager

    Runs the real Qt event loop until the widget provided has been
    deleted.

- :meth:`find_qt_widget`

    Takes parameters ``start``, ``type_`` and ``test``. Recursively walks the Qt
    widget tree from Qt widget ``start`` until it finds a widget of type ``type_``
    (a QWidget subclass) that satisfies the provided ``test`` method.

    Note: This method is known to be finicky / linked to sporadic seg faults.
    The TraitsUI :class:`~traitsui.testing.tester.ui_tester.UITester` is often
    an easier to use, safer alternative if working with a TraitsUI based
    application.

- :meth:`assertEventuallyTrueInGui`

    Assert that the given condition becomes true if we run the GUI
    event loop for long enough.

    This assertion runs the real Qt event loop, polling the condition
    and returning as soon as the condition becomes true. If the condition
    does not become true within the given timeout, the assertion fails.

.. warning::
    Some care needs to be taken with the various methods that run the event
    loop while waiting for a condition function to return true, such as
    :meth:`event_loop_until_condition` and :meth:`assertEventuallyTrueInGui`.
    These work by running the real application event loop and polling for the
    state of the condition being tested.  If the condition being tested is
    transient, it is possible that it may switch from False to True and back to
    False in between polling checks, and so fail to detect that the condition
    occurred.

    When writing tests that use these methods, you should be careful to test
    for conditions that once True, remains True.

For a very simple example consider this (slightly modified) test from pyface's
own test suite.

::

    import unittest

    from pyface.api import Window
    from pyface.util.gui_test_assistant import GuiTestAssistant

    class TestWindow(unittest.TestCase, GuiTestAssistant):
        def setUp(self):
            GuiTestAssistant.setUp(self)
            self.window = Window()

        def tearDown(self):
            if self.window.control is not None:
                with self.delete_widget(self.window.control):
                    self.window.destroy()
            self.window = None
            GuiTestAssistant.tearDown(self)

        def test_open_close(self):
            # test that opening works as expected
            with self.assertTraitChanges(self.window, "opening", count=1):
                with self.assertTraitChanges(self.window, "opened", count=1):
                    with self.event_loop():
                        self.window.open()

            # test that closing works as expected with a different approach
            with self.event_loop_until_traits_change(
                    self.window, "closing", "closed"):
                self.window.close()


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
function taking no arguments which when called opens the modal dialog. From
there you can call the :meth:`open_and_run` method on the tester object just
instantiated, and pass in a ``when_opened`` callable which will take the tester
object as its sole argument. This method first calls the function to open the
dialog and then subsequently the ``when_opened`` callable.  In the body of the
``when_opened`` callable is where you define the interactions with the modal
dialog you want to be performed during the test. You can use the
:meth:`get_dialog_widget` method on the tester object (accesible since the
tester is passed as an argument to ``when_opened``) to get access to the UI for
the dialog. Then interactions can be performed using methods such as
:meth:`find_qt_widget`, :meth:`click_widget`, etc. Alternatively, if working
with a TraitsUI application, you could use the TraitsUI
:class:`~traitsui.testing.tester.ui_tester.UITester` to perform these interactions (see the
`TraitsUI Testing documentation <https://docs.enthought.com/traitsui/traitsui_user_manual/testing.html>`_).
If doing so, it is important to remember to set the :attr:`auto_process_events`
attribute on the :class:`~traitsui.testing.tester.ui_tester.UITester` to False.
This prevents :class:`~traitsui.testing.tester.ui_tester.UITester` and
:class:`ModalDialogTester` from both trying to drive the event loop
simultaneously, which can lead to very strange, difficult to diagnose, bugs.
Finally, you should ensure that your ``when_opened`` callable will close the
dialog.  You don't want to leave the dialog open and blocking (there are
timeouts in place as a safety net, but neverthelesss).
:class:`ModalDialogTester` provides a method :meth:`close` for this purpose.
To verify the dailog was indeed opened once, you can run
``self.assertTrue(tester.dialog_was_opened)``.

Additionally, :class:`ModalDialogTester` provides a context manager
:meth:`capture_error` to be used inside the event loop. When errors or failures
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
