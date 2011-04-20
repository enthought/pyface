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
from traits.api import Any, Interface


class IWidget(Interface):
    """ The base interface for all pyface widgets.

    Pyface widgets delegate to a toolkit specific control.
    """

    #### 'IWidget' interface ##################################################

    # The toolkit specific control that represents the widget.
    control = Any

    # The control's optional parent control.
    parent = Any

    ###########################################################################
    # 'IWidget' interface.
    ###########################################################################

    def destroy(self):
        """ Destroy the control if it exists. """

    ###########################################################################
    # Protected 'IWidget' interface.
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
    # Protected 'IWidget' interface.
    ###########################################################################

    def _create(self):
        self.control = self._create_control(self.parent)

    def _create_control(self, parent):
        raise NotImplementedError

#### EOF ######################################################################
