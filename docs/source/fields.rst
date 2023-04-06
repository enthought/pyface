.. _fields:

======
Fields
======

Pyface provides a small collection of simple field widgets that are pre-bound
to a Traits interface, so that you can use them in a cross-toolkit manner.

Where possible, these classes share a common API for the same functionality.
In particular, all classes have a
:py:attr:`~pyface.fields.i_field.IField.value` trait which holds the value
displayed in the field.

Fields where the value is user-editable rather than simply displayed implement
the :py:attr:`~pyface.fields.i_editable_field.IEditableField` interface.  Code
using the field can listen to changes in the value trait to react to the user
entering a new value for the field without needing to know anything about the
underlying toolkit event signalling mechanisms.

Fields inherit from :py:class:`~pyface.i_widget.IWidget` and
:py:class:`~pyface.i_layout_item.ILayoutItem` which have a number of
additional traits with useful features:

:py:attr:`~pyface.i_widget.IWidget.tooltip`
    A tooltip for the widget, which should hold string.

:py:attr:`~pyface.i_widget.IWidget.context_menu`
    A context menu for the widget, which should hold an
    :py:class:`~pyface.action.i_menu_manager.IMenuManager` instance.

:py:attr:`~pyface.i_layout_item.ILayoutItem.minimum_size`
    A tuple holding the minimum size of a layout widget.

:py:attr:`~pyface.i_layout_item.ILayoutItem.maximum_size`
    A tuple holding the minimum size of a layout widget.

:py:attr:`~pyface.i_layout_item.ILayoutItem.stretch`
    A tuple holding information about the distribution of addtional space into
    the widget when growing in a layout.  Higher numbers mean proportinally
    more space.

:py:attr:`~pyface.i_layout_item.ILayoutItem.size_policy`
    A tuple holding information about how the widget can grow and shrink.

:py:attr:`~pyface.fields.i_field.IField.alignment`
    A value holding the horizontal alignment of the contents of the field.

ComboField
==========

The :py:class:`~pyface.fields.i_combo_field.IComboField` interface has an arbitrary
:py:attr:`~pyface.fields.i_combo_field.IComboField.value` that must come from a list
of valid :py:attr:`~pyface.fields.i_combo_field.IComboField.values`.  For non-text
values, a :py:attr:`~pyface.fields.i_combo_field.IComboField.formatter` function
should be provided, defaulting to :py:func:`str`.

LabelField
==========

The :py:class:`~pyface.fields.i_label_field.ILabelField` interface has a string
for the :py:attr:`~pyface.fields.i_label_field.ILabelField.value` which is not
user-editable.

In the Qt backend they can have an image for an
:py:attr:`~pyface.fields.i_label_field.ILabelField.icon`.

ImageField
==========

The :py:class:`~pyface.fields.i_image_field.IImageField` interface has an
:py:class:`~pyface.i_image.IImage` for its
:py:attr:`~pyface.fields.i_image_field.IImageField.value` which is not
user-editable.

SpinField
=========

The :py:class:`~pyface.fields.i_spin_field.ISpinField` interface has an integer
for the :py:attr:`~pyface.fields.i_spin_field.ISpinField.value`, and also
requires a range to be set, either via setting the min/max values as a tuple to
the :py:attr:`~pyface.fields.i_spin_field.ISpinField.bounds` trait, or by setting
values individually to :py:attr:`~pyface.fields.i_spin_field.ISpinField.minimum`
and :py:attr:`~pyface.fields.i_spin_field.ISpinField.maximum`.  The
:py:attr:`~pyface.fields.i_spin_field.ISpinField.wrap` trait determines whether
the spinner wraps around at the extreme values.

TextField
=========

The :py:class:`~pyface.fields.i_text_field.ITextField` interface provides
additional traits that specify whether the value should be updated on
every keystroke (by setting
:py:attr:`~pyface.fields.i_text_field.ITextField.update_text` to ``"auto"``)
or when the user has finished editing the field by moving focus away from
the text field (by setting
:py:attr:`~pyface.fields.i_text_field.ITextField.update_text` to
``"editing_finshed"``).

The text field can be set to show a placeholder text to hint about the desired
value that is shown when the box is empty via the
:py:attr:`~pyface.fields.i_text_field.ITextField.placeholder` trait.  It can
also be set to conceal typed text by setting
:py:attr:`~pyface.fields.i_text_field.ITextField.echo` to ``"password"`` (and
the Qt backend has a number of other options as well).  The text field can be
set to read-only mode via the
:py:attr:`~pyface.fields.i_text_field.ITextField.read_only` trait.

TimeField
==========

The :py:class:`~pyface.fields.i_time_field.ITimeField` interface has a
:py:class:`datetime.time` :py:attr:`~pyface.fields.i_time_field.ITimeField.value`.
This value defaults to the current time.

ToggleField and Subclasses
==========================

The :py:class:`~pyface.fields.i_toggle_field.IToggleField` interface holds a
boolean :py:attr:`~pyface.fields.i_toggle_field.IToggleField.value` that is
toggled between ``True`` and ``False`` by the widget.  The interface is
implemented by several different concrete classes with different appearances
but similar behaviour:

- :py:class:`~pyface.fields.toggle_field.CheckBoxField`
- :py:class:`~pyface.fields.toggle_field.RadioButtonField`
- :py:class:`~pyface.fields.toggle_field.ToggleButtonField`

There is an abstract class :py:class:`~pyface.fields.toggle_field.ToggleField`
which implements much of the behaviour and is suitable for use by custom
implementations to toggling behaviour.

All :py:class:`~pyface.fields.i_toggle_field.IToggleField` implementations
have can have label text set via the
:py:attr:`~pyface.fields.i_toggle_field.IToggleField.text` trait, and in the
Qt backend they can have an image for an
:py:attr:`~pyface.fields.i_toggle_field.IToggleField.icon`.
