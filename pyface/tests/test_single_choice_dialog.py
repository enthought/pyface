# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import unittest

from traits.etsconfig.api import ETSConfig

from ..single_choice_dialog import SingleChoiceDialog
from ..constant import OK, CANCEL
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"

ModalDialogTester = toolkit_object(
    "util.modal_dialog_tester:ModalDialogTester"
)  # noqa: E501
no_modal_dialog_tester = ModalDialogTester.__name__ == "Unimplemented"

USING_QT = ETSConfig.toolkit not in ["", "wx"]


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestSingleChoiceDialog(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.dialog = SingleChoiceDialog(choices=["red", "blue", "green"])

    def tearDown(self):
        if self.dialog.control is not None:
            with self.delete_widget(self.dialog.control):
                self.dialog.destroy()
        self.dialog = None
        GuiTestAssistant.tearDown(self)

    def test_create(self):
        # test that creation and destruction works as expected
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_destroy(self):
        # test that destroy works even when no control
        with self.event_loop():
            self.dialog.destroy()

    def test_create_cancel(self):
        # test that creation and destruction works no cancel button
        self.dialog.cancel = False
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_create_parent(self):
        # test that creation and destruction works as expected with a parent
        with self.event_loop():
            parent = Window()
            parent.create()
        with self.event_loop():
            self.dialog.create(parent.control)
        with self.event_loop():
            self.dialog.destroy()
        with self.event_loop():
            parent.destroy()

    def test_message(self):
        # test that creation and destruction works as expected with message
        self.dialog.message = "This is the message"
        with self.event_loop():
            self.dialog.create()
        with self.event_loop():
            self.dialog.destroy()

    def test_choice_strings(self):
        # test that choice strings work using simple strings
        self.assertEqual(
            self.dialog._choice_strings(), ["red", "blue", "green"]
        )

    def test_choice_strings_convert(self):
        # test that choice strings work using simple strings
        self.dialog.choices = [1, 2, 3]
        self.assertEqual(self.dialog._choice_strings(), ["1", "2", "3"])

    def test_choice_strings_name_attribute(self):
        # test that choice strings work using attribute name of objects
        class Item(object):
            def __init__(self, description):
                self.description = description

        self.dialog.choices = [Item(name) for name in ["red", "blue", "green"]]
        self.dialog.name_attribute = "description"
        self.assertEqual(
            self.dialog._choice_strings(), ["red", "blue", "green"]
        )

    def test_choice_strings_name_attribute_convert(self):
        # test that choice strings work using attribute name of objects
        class Item(object):
            def __init__(self, description):
                self.description = description

        self.dialog.choices = [Item(name) for name in [1, 2, 3]]
        self.dialog.name_attribute = "description"
        self.assertEqual(self.dialog._choice_strings(), ["1", "2", "3"])

    def test_choice_strings_empty(self):
        # test that choice strings work using simple strings
        self.dialog.choices = []
        with self.assertRaises(ValueError):
            self.dialog._choice_strings()

    def test_choice_strings_duplicated(self):
        # test that choice strings work using simple strings
        self.dialog.choices = ["red", "green", "blue", "green"]
        with self.assertRaises(ValueError):
            self.dialog._choice_strings()

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_accept(self):
        # test that accept works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)
        self.assertEqual(self.dialog.choice, "red")

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_reject(self):
        # test that accept works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=False))

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)
        self.assertIsNone(self.dialog.choice)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_close(self):
        # test that closing works as expected
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(
            when_opened=lambda x: x.get_dialog_widget().close()
        )

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)
        self.assertIsNone(self.dialog.choice)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_parent(self):
        # test that lifecycle works with a parent
        parent = Window()
        self.dialog.parent = parent.control
        parent.open()
        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=lambda x: x.close(accept=True))
        with self.event_loop():
            parent.close()

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_change_choice_accept(self):
        # test that if we change choice it's reflected in result
        def select_green_and_ok(tester):
            control = tester.get_dialog_widget()
            control.setTextValue("green")
            tester.close(accept=True)

        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=select_green_and_ok)

        self.assertEqual(tester.result, OK)
        self.assertEqual(self.dialog.return_code, OK)
        self.assertEqual(self.dialog.choice, "green")

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_change_choice_with_reject(self):
        # test that lifecycle works with a parent
        def select_green_and_cancel(tester):
            control = tester.get_dialog_widget()
            control.setTextValue("green")
            tester.close(accept=False)

        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=select_green_and_cancel)

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)
        self.assertIsNone(self.dialog.choice)

    @unittest.skipIf(no_modal_dialog_tester, "ModalDialogTester unavailable")
    def test_change_choice_with_close(self):
        # test that lifecycle works with a parent
        def select_green_and_close(tester):
            control = tester.get_dialog_widget()
            control.setTextValue("green")
            control.close()

        tester = ModalDialogTester(self.dialog.open)
        tester.open_and_run(when_opened=select_green_and_close)

        self.assertEqual(tester.result, CANCEL)
        self.assertEqual(self.dialog.return_code, CANCEL)
        self.assertIsNone(self.dialog.choice)
