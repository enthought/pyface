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
""" The interface of a workbench editor. """


# Enthought library imports.
from enthought.traits.api import Any, Bool, implements, Instance, Interface
from enthought.traits.api import List, Str, Unicode


class IEditor(Interface):
    """ The interface of a workbench editor. """

    # The optional command stack.
    command_stack = Instance('enthought.undo.api.ICommandStack')

    # The toolkit-specific control that represents the editor.
    #
    # The framework sets this to the value returned by 'create_control'.
    control = Any

##     # Does the editor currently have the focus?
##     has_focus = Bool(False)

    # Is the object that the editor is editing 'dirty' i.e., has it been
    # modified but not saved?
    dirty = Bool(False)

    # The editor's globally unique identifier.
    id = Str

    # The editor's name (displayed to the user).
    name = Unicode

    # The object that the editor is editing.
    #
    # The framework sets this when the editor is created.
    obj = Any

    # The current selection within the editor.
    selection = List

    # The workbench window that the editor is in.
    #
    # The framework sets this when the editor is created.
    window = Instance('IWorkbenchWindow')

    #### Methods ##############################################################
    
    def close(self):
        """ Close the editor.

        This method is not currently called by the framework itself as the user
        is normally in control of the editor lifecycle. Call this if you want
        to control the editor lifecycle programmatically.

        """

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the editor.

        The parameter *parent* is the toolkit-specific control that is the 
        editor's parent.

        Returns the toolkit-specific control.
        
        """

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the editor.

        Returns None.
        
        """

    def set_focus(self):
        """ Set the focus to the appropriate control in the editor.

        Returns None.

        """


class MEditor(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IEditor interface.

    Implements: close(), _command_stack_default()
    """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Return an informal string representation of the object. """

        return 'Editor(%s)' % self.id
    
    ###########################################################################
    # 'IEditor' interface.
    ###########################################################################

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use the name.
        return self.name
    
    def close(self):
        """ Close the editor. """

        if self.control is not None:
            self.window.close_editor(self)

        return

    #### Initializers #########################################################

    def _command_stack_default(self):
        """ Trait initializer. """

        # We make sure the undo package is entirely optional.
        from enthought.undo.api import CommandStack

        return CommandStack(undo_manager=self.window.workbench.undo_manager)

#### EOF ######################################################################
