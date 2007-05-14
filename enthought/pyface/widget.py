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
""" The abstract base class for all Pyface widgets. """


# Enthought library imports.
from enthought.traits.api import Any, HasTraits

# Local imports.
from gui import GUI
from toolkit import patch_toolkit


class Widget(HasTraits):
    """ The abstract base class for all Pyface widgets.

    Pyface widgets delegate to a toolkit specific control.  Note that a widget
    is not necessarily a GUI object.
    """

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

    # FIXME v3: Remove this.
    def invoke_later(self, callable, *args, **kw):
        """ Invokes a callable in the main GUI thread. """

        GUI.invoke_later(callable, *args, **kw)

        return
    
    # FIXME v3: Remove this.
    def set_trait_later(self, obj, trait_name, new):
        """ Sets a trait in the main GUI thread. """

        GUI.set_trait_later(callable, *args, **kw)
        
        return

    ###########################################################################
    # Protected 'Widget' interface.
    ###########################################################################

    def _create(self):
        """ Creates the toolkit specific control. """

        self.control = self._create_control(self.parent)

    # FIXME v3: Why have this and _create()?
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
