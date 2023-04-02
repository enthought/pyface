# (C) Copyright 2007-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# ------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought undo package component>
# ------------------------------------------------------------------------------


# Enthought library imports.
from traits.api import Any, Interface, Str


class ICommand(Interface):
    """The command interface.  The state of the data can be changed by passing
    an instance that implements this interface to the 'push()' method of a
    command stack along with any arguments.
    """

    #### 'ICommand' interface #################################################

    #: This is the data on which the command operates.
    data = Any()

    #: This is the name of the command as it will appear in any GUI element.  It
    #: may include '&' which will be automatically removed whenever it is
    #: inappropriate.
    name = Str()

    ###########################################################################
    # 'ICommand' interface.
    ###########################################################################

    def do(self):
        """This is called by the command stack to do the command and to return
        any value.  The command must save any state necessary for the 'redo()'
        and 'undo()' methods to work.  The class's __init__() must also ensure
        that deep copies of any arguments are made if appropriate.  It is
        guaranteed that this will only ever be called once and that it will be
        called before any call to 'redo()' or 'undo()'.
        """

    def merge(self, other):
        """This is called by the command stack to try and merge another
        command with this one.  True is returned if the commands were merged.
        'other' is the command that is about to be executed.  If the commands
        are merged then 'other' will discarded and not placed on the command
        stack.  A subsequent undo or redo of this modified command must have
        the same effect as the two original commands.
        """

    def redo(self):
        """This is called by the command stack to redo the command.  Any
        returned value will replace the value that the command stack references
        from the original call to 'do()' or previous call to 'redo()'.
        """

    def undo(self):
        """ This is called by the command stack to undo the command. """
