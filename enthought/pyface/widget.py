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
from enthought.traits.api import Any, Interface


class IWidget(Interface):
    """ The base interface for all pyface widgets.

    Pyface widgets delegate to a toolkit specific control.  Note that a widget
    is not necessarily a GUI object.
    """

    #### 'Widget' interface ###################################################

    # The toolkit specific control that represents the widget.
    control = Any

    # The control's optional parent control.
    parent = Any

    ###########################################################################
    # 'Widget' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the control if it exists. """

    ###########################################################################
    # Protected 'Widget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the toolkit specific control. """

    def _create_control(self, parent):
        """ Create and return the toolkit specific control that represents the
        widget.
        """


class MWidget(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IWidget interface.

    Implements: _create()
    """

    ###########################################################################
    # Protected 'Widget' interface.
    ###########################################################################

    def _create(self):
        self.control = self._create_control(self.parent)

    def _create_control(self, parent):
        raise NotImplementedError


# The following will be removed when everything has been moved to interfaces.

# Enthought library imports.
from enthought.traits.api import HasTraits

# Local imports.
from toolkit import patch_toolkit


class Widget(HasTraits):

    __tko__ = 'Widget'

    #### 'Widget' interface ###################################################

    # The toolkit specific control that represents the widget.
    control = Any

    # The control's optional parent control.
    parent = Any

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, *args, **kw):
        """ Initialises a new Widget. """

        HasTraits.__init__(self, *args, **kw)

        patch_toolkit(self)

    ###########################################################################
    # 'Widget' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the control if it exists. """

        if self.control is not None:
            self._tk_widget_destroy()
            self.control = None

    ###########################################################################
    # Protected 'Widget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the toolkit specific control. """

        self.control = self._create_control(self.parent)

    def _create_control(self, parent):
        """ Create and return the toolkit specific control that represents the
        widget.
        """

        return self._tk_widget_create(parent)

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_create(self, parent):
        """ Create and return the toolkit specific control that represents the
        widget.

        This default implementation returns None.
        """

        return None

    def _tk_widget_destroy(self):
        """ Destroy the control.

        This must be reimplemented.
        """

        raise NotImplementedError

#### EOF ######################################################################
