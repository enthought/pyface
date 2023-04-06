# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The base interface for all pyface widgets. """


from traits.api import Any, Bool, HasTraits, Interface, Instance, Str


class IWidget(Interface):
    """ The base interface for all pyface widgets.

    Pyface widgets delegate to a toolkit specific control.
    """

    #: The toolkit specific control that represents the widget.
    control = Any()

    #: The control's optional parent control.
    parent = Any()

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)

    #: A tooltip for the widget.
    tooltip = Str()

    #: An optional context menu for the widget.
    context_menu = Instance("pyface.action.menu_manager.MenuManager")

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        """ Show or hide the widget.

        Parameters
        ----------
        visible : bool
            Visible should be ``True`` if the widget should be shown.
        """

    def enable(self, enabled):
        """ Enable or disable the widget.

        Parameters
        ----------
        enabled : bool
            The enabled state to set the widget to.
        """

    def focus(self):
        """ Set the keyboard focus to this widget.
        """

    def has_focus(self):
        """ Does the widget currently have keyboard focus?

        Returns
        -------
        focus_state : bool
            Whether or not the widget has keyboard focus.
        """

    def create(self, parent=None):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:`control` trait.
        """

    def destroy(self):
        """ Destroy the control if it exists. """

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create_control(self, parent):
        """ Create toolkit specific control that represents the widget.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control to be used as the parent for the widget's
            control.

        Returns
        -------
        control : toolkit control
            A control for the widget.
        """

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """


class MWidget(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWidget interface.
    """

    #: A tooltip for the widget.
    tooltip = Str()

    #: An optional context menu for the widget.
    context_menu = Instance("pyface.action.menu_manager.MenuManager")

    def create(self, parent=None):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        if parent is not None:
            self.parent = parent
        self.control = self._create_control(self.parent)
        self._initialize_control()
        self._add_event_listeners()

    def destroy(self):
        """ Call clean-up code and destroy toolkit objects.

        Subclasses should override to perform any additional clean-up, ensuring
        that they call super() after that clean-up.
        """
        if self.control is not None:
            self._remove_event_listeners()
            self.control = None

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create(self):
        """ Creates the toolkit specific control.

        The default implementation simply calls create()
        """
        from warnings import warn

        warn(
            "The _create() method will be removed in a future version of "
            "Pyface.  Use create() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.create()

    def _create_control(self, parent):
        """ Create toolkit specific control that represents the widget.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control to be used as the parent for the widget's
            control.

        Returns
        -------
        control : toolkit control
            A control for the widget.
        """
        raise NotImplementedError()

    def _initialize_control(self):
        """ Perform any post-creation initialization for the control.
        """
        self._set_control_tooltip(self.tooltip)

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        self.observe(self._tooltip_updated, "tooltip", dispatch="ui")
        self.observe(
            self._context_menu_updated, "context_menu", dispatch="ui"
        )
        if self.control is not None and self.context_menu is not None:
            self._observe_control_context_menu()

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        if self.control is not None and self.context_menu is not None:
            self._observe_control_context_menu(remove=True)
        self.observe(
            self._context_menu_updated,
            "context_menu",
            dispatch="ui",
            remove=True,
        )
        self.observe(
            self._tooltip_updated, "tooltip", dispatch="ui", remove=True
        )

    # Toolkit control interface ---------------------------------------------

    def _get_control_tooltip(self):
        """ Toolkit specific method to get the control's tooltip. """
        raise NotImplementedError()

    def _set_control_tooltip(self, tooltip):
        """ Toolkit specific method to set the control's tooltip. """
        raise NotImplementedError()

    def _observe_control_context_menu(self, remove=False):
        """ Toolkit specific method to change the context menu observer.

        This should use _handle_control_context_menu as the event handler.

        Parameters
        ----------
        remove : bool
            Whether the context menu handler should be removed or added.
        """
        raise NotImplementedError()

    def _handle_control_context_menu(self, event):
        """ Handle a context menu event.

        Implementations should override this with a method suitable to be used
        as a toolkit event handler that invokes a context menu.

        The function signature will likely vary from toolkit to toolkit.
        """
        raise NotImplementedError()

    # Trait change handlers -------------------------------------------------

    def _tooltip_updated(self, event):
        tooltip = event.new
        if self.control is not None:
            self._set_control_tooltip(tooltip)

    def _context_menu_updated(self, event):
        if self.control is not None:
            if event.new is None:
                self._observe_control_context_menu(remove=True)
            if event.old is None:
                self._observe_control_context_menu()
