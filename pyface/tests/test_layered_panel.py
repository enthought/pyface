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

from ..heading_text import HeadingText
from ..layered_panel import LayeredPanel
from ..toolkit import toolkit_object
from ..window import Window

GuiTestAssistant = toolkit_object("util.gui_test_assistant:GuiTestAssistant")
no_gui_test_assistant = GuiTestAssistant.__name__ == "Unimplemented"


@unittest.skipIf(no_gui_test_assistant, "No GuiTestAssistant")
class TestLayeredPanel(unittest.TestCase, GuiTestAssistant):
    def setUp(self):
        GuiTestAssistant.setUp(self)
        self.window = Window()
        self.window.create()

    def tearDown(self):
        if self.widget.control is not None:
            with self.delete_widget(self.widget.control):
                self.widget.destroy()

        if self.window.control is not None:
            with self.delete_widget(self.window.control):
                self.window.destroy()

        del self.widget
        del self.window
        GuiTestAssistant.tearDown(self)

    def test_lifecycle(self):
        # test that create and destory work
        self.widget = LayeredPanel()

        self.assertIsNone(self.widget.control)

        with self.event_loop():
            self.widget.create(parent=self.window.control)

        self.assertIsNotNone(self.widget.control)

        with self.event_loop():
            self.widget.destroy()

        self.assertIsNone(self.widget.control)

    def test_add_layer(self):
        # test that a layer can be added
        self.widget = LayeredPanel()
        layer_widget = HeadingText()

        with self.event_loop():
            self.widget.create(parent=self.window.control)
            layer_widget.create(parent=self.window.control)

        try:
            with self.event_loop():
                self.widget.add_layer("test 1", layer_widget.control)

            self.assertIn("test 1", self.widget._layers)
            self.assertIs(self.widget._layers["test 1"], layer_widget.control)
        finally:
            with self.event_loop():
                layer_widget.destroy()
                self.widget.destroy()

    def test_show_layer(self):
        # test that a layer can be shown
        self.widget = LayeredPanel()
        layer_widget_1 = HeadingText()
        layer_widget_2 = HeadingText()

        with self.event_loop():
            self.widget.create(parent=self.window.control)
            layer_widget_1.create(parent=self.window.control)
            layer_widget_2.create(parent=self.window.control)
            self.widget.add_layer("test 1", layer_widget_1.control)
            self.widget.add_layer("test 2", layer_widget_2.control)

        try:
            with self.event_loop():
                self.widget.show_layer("test 1")

            self.assertEqual(self.widget.current_layer_name, "test 1")
            self.assertIs(self.widget.current_layer, layer_widget_1.control)

            with self.event_loop():
                self.widget.show_layer("test 2")

            self.assertEqual(self.widget.current_layer_name, "test 2")
            self.assertIs(self.widget.current_layer, layer_widget_2.control)
        finally:
            with self.event_loop():
                layer_widget_1.destroy()
                layer_widget_2.destroy()
                self.widget.destroy()

    def test_has_layer(self):
        # test that a has_layer works
        self.widget = LayeredPanel()
        layer_widget_1 = HeadingText()
        layer_widget_2 = HeadingText()

        with self.event_loop():
            self.widget.create(parent=self.window.control)
            layer_widget_1.create(parent=self.window.control)
            layer_widget_2.create(parent=self.window.control)
            self.widget.add_layer("test 1", layer_widget_1.control)
            self.widget.add_layer("test 2", layer_widget_2.control)

        try:
            self.assertTrue(self.widget.has_layer("test 1"))
            self.assertTrue(self.widget.has_layer("test 2"))
        finally:
            with self.event_loop():
                layer_widget_1.destroy()
                layer_widget_2.destroy()

        with self.event_loop():
            self.widget.destroy()
