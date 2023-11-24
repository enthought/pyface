# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Test for pyface.api """

import unittest

from traits.etsconfig.api import ETSConfig

is_wx = (ETSConfig.toolkit == 'wx')
is_qt = ETSConfig.toolkit.startswith('qt')


class TestApi(unittest.TestCase):
    """ Test importable items in any environment."""

    def test_api_importable(self):
        # make sure api is importable with the most minimal
        # required dependencies, including in the absence of toolkit backends.
        from pyface import api   # noqa: F401

    def test_public_attrs(self):
        # make sure everything advertised by dir() is available except optional
        from pyface import api

        attrs = [
            name
            for name in dir(api)
            if not (name.startswith('_') or name in api._optional_imports)
        ]
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertIsNotNone(getattr(api, attr, None))


@unittest.skipIf(not is_qt, "This test is for qt.")
class TestApiQt(unittest.TestCase):
    """ Test importable items in a Qt environment."""

    def test_importable_items_minimal(self):
        # Test items should be importable in a minimal Qt environment
        # Pygments is excused. Attempt to import PythonEditor or PythonShell
        # will fail in an environment without pygments, just as it
        # would if these items were imported directly from the corresponding
        # subpackages.
        from pyface.api import (   # noqa: F401
            AboutDialog,
            Alignment,
            Application,
            ApplicationWindow,
            Border,
            BaseDropHandler,
            CANCEL,
            Clipboard,
            ConfirmationDialog,
            Dialog,
            DirectoryDialog,
            ExpandablePanel,
            FileDialog,
            FileDropHandler,
            Filter,
            GUI,
            GUIApplication,
            HasBorder,
            HasMargin,
            HeadingText,
            Image,
            ImageCache,
            ImageResource,
            ImageWidget,
            KeyPressedEvent,
            LayeredPanel,
            MDIApplicationWindow,
            MDIWindowMenu,
            Margin,
            MessageDialog,
            MultiToolbarWindow,
            NO,
            OK,
            ProgressDialog,
            # PythonEditor and PythonShell are omitted
            SingleChoiceDialog,
            Sorter,
            SplashScreen,
            SplitApplicationWindow,
            SplitDialog,
            SplitPanel,
            SystemMetrics,
            Widget,
            Window,
            YES,
            beep,
            choose_one,
            clipboard,
            confirm,
            error,
            information,
            warning,
            # Interfaces
            IAboutDialog,
            IApplicationWindow,
            IClipboard,
            IConfirmationDialog,
            IDialog,
            IDirectoryDialog,
            IDropHandler,
            IFileDialog,
            IGUI,
            IHeadingText,
            IImage,
            IImageResource,
            ILayeredPanel,
            ILayoutItem,
            ILayoutWidget,
            IMessageDialog,
            IPILImage,
            IProgressDialog,
            IPythonEditor,
            IPythonShell,
            ISingleChoiceDialog,
            ISplashScreen,
            ISplitWidget,
            ISystemMetrics,
            IWidget,
            IWindow,
        )

    def test_python_editor_python_shell_importable(self):
        # If pygments is in the environment, PythonEditor and PythonShell
        # should be importable.
        try:
            import pygments        # noqa: F401
        except ImportError:
            raise self.skipTest("This test requires pygments.")

        from pyface.api import (   # noqa: F401
            PythonEditor,
            PythonShell,
        )


@unittest.skipIf(not is_wx, "This test is for wx.")
class TestApiWx(unittest.TestCase):
    """ Test importable items in a wx environment."""

    def test_importable_items(self):
        # These items should always be importable for wx environment
        from pyface.api import (   # noqa: F401
            AboutDialog,
            Alignment,
            Application,
            ApplicationWindow,
            Border,
            CANCEL,
            Clipboard,
            ConfirmationDialog,
            BaseDropHandler,
            Dialog,
            DirectoryDialog,
            ExpandablePanel,
            FileDialog,
            FileDropHandler,
            Filter,
            GUI,
            GUIApplication,
            HasBorder,
            HasMargin,
            HeadingText,
            Image,
            ImageCache,
            ImageResource,
            ImageWidget,
            KeyPressedEvent,
            LayeredPanel,
            MDIApplicationWindow,
            MDIWindowMenu,
            Margin,
            MessageDialog,
            MultiToolbarWindow,
            NO,
            OK,
            ProgressDialog,
            PythonEditor,
            PythonShell,
            SingleChoiceDialog,
            Sorter,
            SplashScreen,
            SplitApplicationWindow,
            SplitDialog,
            SplitPanel,
            SystemMetrics,
            Widget,
            Window,
            YES,
            beep,
            choose_one,
            clipboard,
            confirm,
            error,
            information,
            warning,
            # Interfaces
            IAboutDialog,
            IApplicationWindow,
            IClipboard,
            IConfirmationDialog,
            IDialog,
            IDirectoryDialog,
            IDropHandler,
            IFileDialog,
            IGUI,
            IHeadingText,
            IImageResource,
            ILayeredPanel,
            ILayoutItem,
            ILayoutWidget,
            IMessageDialog,
            IProgressDialog,
            IPILImage,
            IPythonEditor,
            IPythonShell,
            ISingleChoiceDialog,
            ISplashScreen,
            ISplitWidget,
            ISystemMetrics,
            IWindow,
            IWidget,
        )
