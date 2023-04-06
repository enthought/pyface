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
- :func:`~.find_toolkit`
- :class:`~.GUI`
- :class:`~.GUIApplication`
- :class:`~.ImageResource`
- :class:`~.KeyPressedEvent`
- :class:`~.SplashScreen`
- :class:`~.SplitApplicationWindow`
- :class:`~.SplitPanel`
- :class:`~.SystemMetrics`
- :class:`~.Toolkit`
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
- :class:`~.HasBorder`
- :class:`~.HasMargin`
- :class:`~.Image`
- :attr:`~.Orientation`
- :attr:`~.Position`
- :class:`~.PyfaceColor`
- :class:`~.PyfaceFont`

Miscellaneous
-------------

- :class:`~.ArrayImage`
- :class:`~.BaseDropHandler`
- :class:`~.Border`
- :class:`~.beep`
- :class:`~.FileDropHandler`
- :class:`~.Filter`
- :class:`~.HeadingText`
- :class:`~.ImageCache`
- :class:`~.LayeredPanel`
- :class:`~.Margin`
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

# Imports which don't select the toolkit as a side-effect.

from .application import Application
from .base_toolkit import Toolkit, find_toolkit
from .color import Color
from .constant import OK, CANCEL, YES, NO
from .filter import Filter
from .font import Font
from .gui_application import GUIApplication
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
from .sorter import Sorter
from .ui_traits import (
    Alignment, Border, HasBorder, HasMargin, Image, Margin, Orientation,
    Position, PyfaceColor, PyfaceFont
)

# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

_toolkit_imports = {
    'AboutDialog': 'about_dialog',
    'ApplicationWindow': "application_window",
    'BaseDropHandler': "drop_handler",
    'beep': "beep",
    'Clipboard': "clipboard",
    'ConfirmationDialog': "confirmation_dialog",
    'Dialog': "dialog",
    'DirectoryDialog': "directory_dialog",
    'FileDropHandler': "drop_handler",
    'FileDialog': "file_dialog",
    'GUI': 'gui',
    'HeadingText': "heading_text",
    'ImageCache': "image_cache",
    'ImageResource': "image_resource",
    'KeyPressedEvent': "key_pressed_event",
    'LayeredPanel': "layered_panel",
    'MessageDialog': "message_dialog",
    'ProgressDialog': "progress_dialog",
    'SingleChoiceDialog': "single_choice_dialog",
    'SplashScreen': "splash_screen",
    'SystemMetrics': "system_metrics",
    'Window': "window",
    'Widget': "widget",

    # Wx-only (or legacy) imports
    'ExpandablePanel': "expandable_panel",
    'ImageWidget': "image_widget",
    'MDIApplicationWindow': "mdi_application_window",
    'MDIWindowMenu': "mdi_window_menu",
    'MultiToolbarWindow': "multi_toolbar_window",
}

# These are pyface.* imports that have selection as a side-effect
# TODO: refactor to delay imports where possible
_relative_imports = {
    'choose_one': "single_choice_dialog",
    'clipboard': "clipboard",
    'confirm': "confirmation_dialog",
    'error': "message_dialog",
    'information': "message_dialog",
    'SplitApplicationWindow': "split_application_window",
    'SplitDialog': "split_dialog",
    'SplitPanel': "split_panel",
    'warning': "message_dialog",
}
_optional_imports = {
    'ArrayImage': ("numpy", "array_image"),
    'PILImage': ("pillow", "pil_image"),
    'PythonEditor': ("pygments", "python_editor"),
    'PythonShell': ("pygments", "python_shell"),
}


def __getattr__(name):
    """Lazily load attributes with side-effects

    In particular, lazily load toolkit backend names.  For efficiency, lazily
    loaded objects are injected into the module namespace
    """
    # sentinel object for no result
    not_found = object()
    result = not_found

    if name in _relative_imports:
        from importlib import import_module
        source = _relative_imports[name]
        module = import_module(f"pyface.{source}")
        result = getattr(module, name)

    elif name in _toolkit_imports:
        from pyface.toolkit import toolkit_object
        source = _toolkit_imports[name]
        result = toolkit_object(f"{source}:{name}")

    elif name in _optional_imports:
        from importlib import import_module
        import logging
        from pyface.util._optional_dependencies import optional_import
        dependency, source = _optional_imports[name]
        with optional_import(
            dependency,
            msg=f"{name} is not available due to missing {dependency}.",
            logger=logging.getLogger(__name__),
        ):
            module = import_module(f"pyface.{source}")
            result = getattr(module, name)

    if result is not_found:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    globals()[name] = result
    return result


# ----------------------------------------------------------------------------
# Introspection support
# ----------------------------------------------------------------------------

# the list of available names we report for introspection purposes
_extra_names = (
    set(_toolkit_imports) | set(_relative_imports) | set(_optional_imports)
)


def __dir__():
    return sorted(set(globals()) | _extra_names)
