#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" The base interface for all pyface widgets. """


# Enthought library imports.
from traits.api import Any, Bool, HasTraits, Interface


class IWidget(Interface):
    """ The base interface for all pyface widgets.

    Pyface widgets delegate to a toolkit specific control.
    """

    #: The toolkit specific control that represents the widget.
    control = Any

    #: The control's optional parent control.
    parent = Any

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)

    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        """ Show or hide the widget.

        Parameter
        ---------
        visible : bool
            Visible should be ``True`` if the widget should be shown.
        """

    def enable(self, enabled):
        """ Enable or disable the widget.

        Parameter
        ---------
        enabled : bool
            The enabled state to set the widget to.
        """

    def destroy(self):
        """ Destroy the control if it exists. """

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create(self):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """

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


class MWidget(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWidget interface.
    """

    # ------------------------------------------------------------------------
    # Protected 'IWidget' interface.
    # ------------------------------------------------------------------------

    def _create(self):
        """ Creates the toolkit specific control.

        This method should create the control and assign it to the
        :py:attr:``control`` trait.
        """
        self.control = self._create_control(self.parent)
        self._add_event_listeners()

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
        raise NotImplementedError

    def _add_event_listeners(self):
        """ Set up toolkit-specific bindings for events """
        pass

    def _remove_event_listeners(self):
        """ Remove toolkit-specific bindings for events """
        pass
