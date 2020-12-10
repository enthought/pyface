.. _widgets:

=======
Widgets
=======

.. py:currentmodule:: pyface

A Widget in Pyface is an object wraps a control from the underlying toolkit
and provides standard traits and methods that abstract the differences
between the interfaces presented by the toolkit widgets.

The public API for every widget is provided by the appropriate interface
class: :class:`~pyface.i_widget.IWidget` and its subclasses such as
:class:`~pyface.i_application_window.IApplicationWindow` and
:class:`~pyface.fields.i_text_field.ITextField`.

The actual implementation is provided by the corresponding toolkit-dependent
:class:`~pyface.widget.Widget` subclass, but with shared functionality split
into separate mixins: :class:`~pyface.i_widget.MWidget` and so on, following
the general design described in the :ref:`overview` section.

Lifecycle
=========

When a :class:`~pyface.widget.Widget` instance is created only the traits
are initialized.  The underlying toolkit widget is not created until the
widget's :meth:`~pyface.widget.Widget._create` method is called, which is
responsible for creating the toolkit object, configuring it, and connecting
handlers that react to changes at the toolkit level or on the traits,
keeping the state of the Python class synchronised with the state of the
underlying toolkit object.  The :meth:`~pyface.widget.Widget._create` method
calls the :meth:`~pyface.widget.Widget._create_control` method to create the
actual toolkit control and configure it, and also calls the
:meth:`~pyface.widget.Widget._add_event_listeners` method to handle hooking
up the different types of change handlers.  Some widget subclasses may do
additional things in their :meth:`~pyface.widget.Widget._create` methods,
as appropriate for their purpose.

To destroy the toolkit object, the :meth:`~pyface.widget.Widget.destroy`
method is called which cleans up the code that listens for changes to the
object, and destroys the underlying toolkit control (and, for most toolkits,
any children).  The :meth:`~pyface.widget.Widget.destroy` method
calls the :meth:`~pyface.widget.Widget._remove_event_listeners` method to
handle unhooking of change handlers.  Some widget subclasses may do
additional things in their :meth:`~pyface.widget.Widget.destroy` methods.

Basic Interface
===============

Every widget has a :attr:`~pyface.i_widget.IWidget.control` trait which
holds a reference to the toolkit control that is actually doing the work.
Additionally, there is a :attr:`~pyface.i_widget.IWidget.parent` trait
which references the toolkit control which is the parent of the widget's
control, however this may be ``None`` for top-level windows.

Additionally, every widget has two states associated with it: it can be
visible or hidden, and it can be enabled or disabled.  The visibile
state is accessible via the :attr:`~pyface.i_widget.IWidget.visible`
trait, or by calling :meth:`~pyface.i_widget.IWidget.show`.  Similarly
the enabled state is accessible via the
:attr:`~pyface.i_widget.IWidget.enabled` trait, or by calling
:meth:`~pyface.i_widget.IWidget.enable`.

IWidget Subclasses
==================

The key subclasses/subinterfaces of :class:`~pyface.i_widget.IWidget` include
the following.

IWindow
-------

The :class:`~pyface.i_window.IWindow` interface represents a top-level
window, and so provides additional traits such as
:attr:`~pyface.i_window.IWindow.size`,
:attr:`~pyface.i_window.IWindow.position` and
:attr:`~pyface.i_window.IWindow.title`, as well as events for the
window's lifecycle and user interactions.

The :meth:`~pyface.i_window.IWindow.open` and
:meth:`~pyface.i_window.IWindow.close` methods provide the standard
way of bring up non-modal windows and closing them with the option of
a user veto.

Additionally there are convenience methods that create message dialogs
correctly parented to the window.

IDialog
-------

The :class:`~pyface.i_dialog.IDialog` interface represents short-lived,
usually modal, dialog windows.  Often these are standard system dialogs,
in which case the class is responsible for configuring and invoking them,
but it also includes subclasses which have custom content.

For modal dialogs, :meth:`~pyface.i_dialog.IDialog.open` is blocking,
and returns the :attr:`~pyface.i_dialog.IDialog.return_code` of the
dialog after the user is done.  Typical usage looks like::

    dialog = MyModalDialog()
    if dialog.open() == OK:
        # do something based on dialog state
        ...
    else:
        # user cancelled, clean-up if needed and stop
        ...

For custom dialogs, there are protected methods for creating the contents
of the dialog and its buttons.  In most cases you will need to, at a minimum,
override the :meth:`~pyface.i_dialog.IDialog._create_dialog_area` method to
populate the widgets inside the main dialog.

IApplicationWindow
------------------

The :class:`~pyface.i_application_window.IApplicationWindow` interface
represents a main window of an application with the associated additional
features which go with these, such as menubars, toolbars, and status bars.
Users can supply
:attr:`~pyface.i_application_window.IApplicationWindow.menu_bar_manager`,
:attr:`~pyface.i_application_window.IApplicationWindow.status_bar_manager`
and :attr:`~pyface.i_application_window.IApplicationWindow.tool_bar_managers`
objects to provide the functionality, and the concrete implementations will
use these to create the toolkit-level objects.

Writers of custom subclasses will have to override the
:meth:`~pyface.i_application_window.IApplicationWindow._create_contents`
method to populate the actual contents of the window.

IField
------

The :class:`~pyface.fields.i_field.IField` interface is the base for widgets
which present a value to be edited by the user, such as text fields, sliders,
combo-boxes and so on.  The interface is described in more detail in the
section on :ref:`fields`.
