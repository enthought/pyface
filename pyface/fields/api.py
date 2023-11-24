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

API for the ``pyface.fields`` subpackage.

- :class:`~.CheckBoxField`
- :class:`~.ComboField`
- :class:`~.EditableField`
- :class:`~.Field`
- :class:`~.ImageField`
- :class:`~.LabelField`
- :class:`~.RadioButtonField`
- :class:`~.SpinField`
- :class:`~.TextField`
- :class:`~.TimeField`
- :class:`~.ToggleButtonField`

Interfaces
----------
- :class:`~.IComboField`
- :class:`~.IEditableField`
- :class:`~.IField`
- :class:`~.IImageField`
- :class:`~.ILabelField`
- :class:`~.ISpinField`
- :class:`~.ITextField`
- :class:`~.ITimeField`
- :class:`~.IToggleField`

"""

from .i_combo_field import IComboField
from .i_editable_field import IEditableField
from .i_field import IField
from .i_image_field import IImageField
from .i_label_field import ILabelField
from .i_spin_field import ISpinField
from .i_text_field import ITextField
from .i_time_field import ITimeField
from .i_toggle_field import IToggleField


# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

_toolkit_imports = {
    'CheckBoxField': 'toggle_field',
    'ComboField': 'combo_field',
    'EditableField': 'editable_field',
    'Field': 'field',
    'ImageField': 'image_field',
    'LabelField': 'label_field',
    'RadioButtonField': 'toggle_field',
    'SpinField': 'spin_field',
    'TextField': 'text_field',
    'TimeField': 'time_field',
    'ToggleButtonField': 'toggle_field',
}


def __getattr__(name):
    """Lazily load attributes with side-effects

    In particular, lazily load toolkit backend names.  For efficiency, lazily
    loaded objects are injected into the module namespace
    """
    # sentinel object for no result
    not_found = object()
    result = not_found

    if name in _toolkit_imports:
        from pyface.toolkit import toolkit_object
        source = _toolkit_imports[name]
        result = toolkit_object(f"fields.{source}:{name}")

    if result is not_found:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    globals()[name] = result
    return result


# ----------------------------------------------------------------------------
# Introspection support
# ----------------------------------------------------------------------------

def __dir__():
    return sorted(set(globals()) | set(_toolkit_imports))
