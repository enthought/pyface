# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.testing.widget_mixin import WidgetMixin


class LayoutWidgetMixin(WidgetMixin):
    """ Test mixin for classes which inherit LayoutWidget. """

    def test_minimum_size(self):
        # create a widget with a minimum size
        self.widget.minimum_size = (100, 100)
        self.widget.create()
        minimum_size = self.widget._get_control_minimum_size()
        self.gui.process_events()
        self.assertEqual(minimum_size, (100, 100))

        # change the minimum size
        self.widget.minimum_size = (50, 50)
        self.gui.process_events()
        minimum_size = self.widget._get_control_minimum_size()

        self.assertEqual(minimum_size, (50, 50))

    def test_maximum_size(self):
        # create a widget with a maximum size
        self.widget.maximum_size = (1000, 1000)
        self.widget.create()
        maximum_size = self.widget._get_control_maximum_size()
        self.gui.process_events()
        self.assertEqual(maximum_size, (1000, 1000))

        # change the maximum size
        self.widget.maximum_size = (50, 50)
        self.gui.process_events()
        maximum_size = self.widget._get_control_maximum_size()

        self.assertEqual(maximum_size, (50, 50))

    def test_stretch(self):
        # create a widget with a maximum size
        self.widget.stretch = (2, 3)
        self.widget.create()
        stretch = self.widget._get_control_stretch()
        self.gui.process_events()
        self.assertEqual(stretch, (2, 3))

        # change the maximum size
        self.widget.stretch = (5, 0)
        self.gui.process_events()
        maximum_size = self.widget._get_control_stretch()

        self.assertEqual(maximum_size, (5, 0))

    def test_size_policy(self):
        # create a widget with a maximum size
        self.widget.create()
        self.assertEqual(
            self.widget._get_control_size_policy(),
            ("default", "default"),
        )

        for horizontal in ["fixed", "preferred", "expand"]:
            for vertical in ["fixed", "preferred", "expand"]:
                with self.subTest(horizontal=horizontal, vertical=vertical):
                    self.widget.size_policy = (horizontal, vertical)
                    self.gui.process_events()
                    self.assertEqual(
                        self.widget._get_control_size_policy(),
                        (horizontal, vertical),
                    )
