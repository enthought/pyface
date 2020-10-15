.. _fields:

======
Fields
======

Pyface provides a small collection of simple field widgets that are pre-bound
to a Traits interface, so that you can use them in a cross-toolkit manner.

Where possible, these classes share a common API for the same functionality.
In particular, all classes have a
:py:attr:`~pyface.fields.i_field.IField.value` trait which holds the (usually
user-editable) value displayed in the field.  Code using the field can listen
to changes in this trait to react to the user entering a new value for the
field without needing to know anything about the underlying toolkit event
signalling mechanisms.

All fields also provide traits for setting the
:py:attr:`~pyface.fields.i_field.IField.tooltip` and
:py:attr:`~pyface.fields.i_field.IField.context_menu` of the field.  Tooltips
expect unicode text values, and context menus should be
:py:class:`~pyface.action.menu_manager.MenuManager` instances.

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

SpinField
=========

The :py:class:`~pyface.fields.i_spin_field.ISpinField` interface has an integer
for the :py:attr:`~pyface.fields.i_spin_field.ISpinField.value`, and also
requires a range to be set, either via setting the min/max values as a tuple to
the :py:attr:`~pyface.fields.i_spin_field.ISpinField.range` trait, or by setting
values individually to :py:attr:`~pyface.fields.i_spin_field.ISpinField.minimum`
and :py:attr:`~pyface.fields.i_spin_field.ISpinField.maximum`.

ComboField
==========

The :py:class:`~pyface.fields.i_combo_field.IComboField` interface has an arbitrary
:py:attr:`~pyface.fields.i_spin_field.IComboField.value` that must come from a list
of valid :py:attr:`~pyface.fields.i_spin_field.IComboField.values`.  For non-text
values, a :py:attr:`~pyface.fields.i_spin_field.IComboField.formatter` function
should be provided - this defaults to either :py:func:`str` (Python 3+) or
:py:func:`unicode` (Python 2).


