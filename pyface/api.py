# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""

API for the ``pyface`` package.

- :class:`~.Application`
- :class:`~.ApplicationWindow`
- :attr:`~.clipboard`
- :class:`~.Clipboard`
- :class:`~.GUI`
- :class:`~.GUIApplication`
- :class:`~.ImageResource`
- :class:`~.KeyPressedEvent`
- :class:`~.SplashScreen`
- :class:`~.SplitApplicationWindow`
- :class:`~.SplitPanel`
- :class:`~.SystemMetrics`
- :class:`~.Window`
- :class:`~.Widget`

Dialogs
-------

- :class:`~.AboutDialog`
- :class:`~.confirm`
- :class:`~.ConfirmationDialog`
- :class:`~.Dialog`
- :class:`~.DirectoryDialog`
- :class:`~.FileDialog`
- :class:`~.error`
- :class:`~.information`
- :class:`~.warning`
- :class:`~.MessageDialog`
- :class:`~.ProgressDialog`
- :class:`~.choose_one`
- :class:`~.SingleChoiceDialog`
- :class:`~.SplitDialog`

Interfaces
----------

- :class:`~.IAboutDialog`
- :class:`~.IApplicationWindow`
- :class:`~.IClipboard`
- :class:`~.IConfirmationDialog`
- :class:`~.IDialog`
- :class:`~.IDirectoryDialog`
- :class:`~.IDropHandler`
- :class:`~.IFileDialog`
- :class:`~.IGUI`
- :class:`~.IHeadingText`
- :class:`~.IImage`
- :class:`~.IImageResource`
- :class:`~.ILayeredPanel`
- :class:`~.ILayoutItem`
- :class:`~.ILayoutWidget`
- :class:`~.IMessageDialog`
- :class:`~.IPILImage`
- :class:`~.IProgressDialog`
- :class:`~.IPythonEditor`
- :class:`~.IPythonShell`
- :class:`~.ISingleChoiceDialog`
- :class:`~.ISplashScreen`
- :class:`~.ISplitWidget`
- :class:`~.ISystemMetrics`
- :class:`~.IWidget`
- :class:`~.IWindow`

Constants
---------

- :class:`~.OK`
- :class:`~.CANCEL`
- :class:`~.YES`
- :class:`~.NO`

UI Traits
---------

- :attr:`~.Alignment`
- :class:`~.Border`
- :class:`~.HasBorder`
- :class:`~.HasMargin`
- :class:`~.Image`
- :class:`~.Margin`

Miscellaneous
-------------

- :class:`~.ArrayImage`
- :class:`~.BaseDropHandler`
- :class:`~.beep`
- :class:`~.FileDropHandler`
- :class:`~.Filter`
- :class:`~.HeadingText`
- :class:`~.ImageCache`
- :class:`~.LayeredPanel`
- :class:`~.PILImage`
- :class:`~.PythonEditor`
- :class:`~.PythonShell`
- :class:`~.Sorter`

Note that the :class:`~.ArrayImage` is only available if the ``numpy``
package is available in the Python environment.

Note that the :class:`~.PILImage` is only available if the ``pillow``
package is available in the Python environment.

Note that the :class:`~.PythonEditor` and :class:`~.PythonShell` classes are
only available if the ``pygments`` package is available in the Python
environment.

Wx-specific classes
-------------------

- :class:`~.ExpandablePanel`
- :class:`~.ImageWidget`
- :class:`~.MDIApplicationWindow`
- :class:`~.MDIWindowMenu`
- :class:`~.MultiToolbarWindow`

"""

import logging as _logging

from .about_dialog import AboutDialog
from .application import Application
from .application_window import ApplicationWindow
from .beep import beep
from .clipboard import clipboard, Clipboard
from .confirmation_dialog import confirm, ConfirmationDialog
from .constant import OK, CANCEL, YES, NO
from .dialog import Dialog
from .directory_dialog import DirectoryDialog
from .drop_handler import BaseDropHandler, FileDropHandler
from .file_dialog import FileDialog
from .filter import Filter
from .gui import GUI
from .gui_application import GUIApplication
from .heading_text import HeadingText
from .image_cache import ImageCache
from .image_resource import ImageResource
from .key_pressed_event import KeyPressedEvent
from .layered_panel import LayeredPanel
from .message_dialog import error, information, warning, MessageDialog
from .progress_dialog import ProgressDialog

from .util._optional_dependencies import optional_import as _optional_import

# Excuse numpy dependency, otherwise re-raise
with _optional_import(
        "numpy",
        msg="ArrayImage not available due to missing numpy.",
        logger=_logging.getLogger(__name__)):

    # We need to manually try importing numpy because the ``ArrayImage``
    # import will end up raising a ``TraitError`` exception instead of an
    # ``ImportError``, which isnt caught by ``_optional_import``.
    import numpy

    from .array_image import ArrayImage

    del numpy

# Excuse pillow dependency, otherwise re-raise
with _optional_import(
        "pillow",
        msg="PILImage not available due to missing pillow.",
        logger=_logging.getLogger(__name__)):
    from .pil_image import PILImage

# Excuse pygments dependency (for Qt), otherwise re-raise
with _optional_import(
        "pygments",
        msg="PythonEditor not available due to missing pygments.",
        logger=_logging.getLogger(__name__)):
    from .python_editor import PythonEditor

with _optional_import(
        "pygments",
        msg="PythonShell not available due to missing pygments.",
        logger=_logging.getLogger(__name__)):
    from .python_shell import PythonShell

from .sorter import Sorter
from .single_choice_dialog import choose_one, SingleChoiceDialog
from .splash_screen import SplashScreen
from .split_application_window import SplitApplicationWindow
from .split_dialog import SplitDialog
from .split_panel import SplitPanel
from .system_metrics import SystemMetrics
from .ui_traits import Alignment, Border, HasBorder, HasMargin, Image, Margin
from .window import Window
from .widget import Widget

# ----------------------------------------------------------------------------
# Public Interfaces
# ----------------------------------------------------------------------------

from .i_about_dialog import IAboutDialog
from .i_application_window import IApplicationWindow
from .i_clipboard import IClipboard
from .i_confirmation_dialog import IConfirmationDialog
from .i_dialog import IDialog
from .i_directory_dialog import IDirectoryDialog
from .i_drop_handler import IDropHandler
from .i_file_dialog import IFileDialog
from .i_gui import IGUI
from .i_heading_text import IHeadingText
from .i_image import IImage
from .i_image_resource import IImageResource
from .i_layered_panel import ILayeredPanel
from .i_layout_item import ILayoutItem
from .i_layout_widget import ILayoutWidget
from .i_message_dialog import IMessageDialog
from .i_pil_image import IPILImage
from .i_progress_dialog import IProgressDialog
from .i_python_editor import IPythonEditor
from .i_python_shell import IPythonShell
from .i_single_choice_dialog import ISingleChoiceDialog
from .i_splash_screen import ISplashScreen
from .i_split_widget import ISplitWidget
from .i_system_metrics import ISystemMetrics
from .i_widget import IWidget
from .i_window import IWindow

# ----------------------------------------------------------------------------
# Legacy and Wx-specific imports.
# ----------------------------------------------------------------------------

# These widgets currently only have Wx implementations
# will return Unimplemented for Qt.

from .expandable_panel import ExpandablePanel
from .image_widget import ImageWidget
from .mdi_application_window import MDIApplicationWindow
from .mdi_window_menu import MDIWindowMenu
from .multi_toolbar_window import MultiToolbarWindow

# This code isn't toolkit widget code, but is wx-specific
from traits.etsconfig.api import ETSConfig

if ETSConfig.toolkit == "wx":

    # Fix for broken Pycrust introspect module.
    # XXX move this somewhere better? - CJW 2017
    from .util import fix_introspect_bug

del ETSConfig
