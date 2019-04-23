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
""" The base class for all actions. """

from functools import partial

# Enthought library imports.
from traits.api import Bool, Callable, Enum, HasTraits, Str
from traits.api import Unicode

from pyface.ui_traits import Image


class Action(HasTraits):
    """ The base class for all actions.

    An action is the non-UI side of a command which can be triggered by the end
    user.  Actions are typically associated with buttons, menu items and tool
    bar tools.

    When the user triggers the command via the UI, the action's 'perform'
    method is invoked to do the actual work.

    """

    #### 'Action' interface ###################################################

    #: Keyboard accelerator (by default the action has NO accelerator).
    accelerator = Unicode

    #: Is the action checked?  This is only relevant if the action style is
    #: 'radio' or 'toggle'.
    checked = Bool(False)

    #: A longer description of the action (used for context sensitive help etc).
    #: If no description is specified, the tooltip is used instead (and if there
    #: is no tooltip, then well, maybe you just hate your users ;^).
    description = Unicode

    #: Is the action enabled?
    enabled = Bool(True)

    #: Is the action visible?
    visible = Bool(True)

    #: The action's unique identifier (may be None).
    id = Str

    #: The action's image (displayed on tool bar tools etc).
    image = Image

    #: The action's name (displayed on menus/tool bar tools etc).
    name = Unicode

    #: An (optional) callable that will be invoked when the action is performed.
    on_perform = Callable

    #: The action's style.
    style = Enum('push', 'radio', 'toggle', 'widget')

    #: A short description of the action used for tooltip text etc.
    tooltip = Unicode

    #: An (optional) callable to create the toolkit control for widget style.
    control_factory = Callable

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Initializes the 'id' trait.

        The default is the ``name`` trait.
        """
        return self.name

    #### Methods ##############################################################

    def create_control(self, parent):
        """ Called when creating a "widget" style action.

        By default this will call whatever callable is supplied via the
        'control_factory' trait which is a callable that should take the parent
        control and the action as arguments and return an appropriate toolkit
        control.  Some operating systems (Mac OS in particular) may limit what
        widgets can be displayed in menus.

        This method is only used when the 'style' is "widget" and is ignored by
        other styles.

        Parameters
        ----------
        parent : toolkit control
            The toolkit control, usually a toolbar.

        Returns
        -------
        control : toolkit control
            A toolkit control or None.
        """
        if self.style == 'widget' and self.control_factory is not None:
            return self.control_factory(parent, self)
        return None

    def destroy(self):
        """ Called when the action is no longer required.

        By default this method does nothing, but this would be a great place to
        unhook trait listeners etc.
        """

    def perform(self, event):
        """ Performs the action.

        Parameters
        ----------
        event : ActionEvent instance
            The event which triggered the action.
        """
        if self.on_perform is not None:
            self.on_perform()

    @classmethod
    def factory(cls, *args, **kwargs):
        """ Create a factory for an action with the given arguments.

        This is particularly useful for passing context to Tasks schema
        additions.
        """
        return partial(cls, *args, **kwargs)