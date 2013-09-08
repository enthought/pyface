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
""" The interface for workbench parts. """


# Enthought library imports.
from traits.api import Any, Bool, HasTraits, Instance, Interface
from traits.api import List, provides, Str, Unicode


class IWorkbenchPart(Interface):
    """ The interface for workbench parts.

    A workbench part is a visual section within the workbench. There are two
    sub-types, 'View' and 'Editor'.

    """

    # The toolkit-specific control that represents the part.
    #
    # The framework sets this to the value returned by 'create_control'.
    control = Any

    # Does the part currently have the focus?
    has_focus = Bool(False)

    # The part's globally unique identifier.
    id = Str

    # The part's name (displayed to the user).
    name = Unicode

    # The current selection within the part.
    selection = List

    # The workbench window that the part is in.
    #
    # The framework sets this when the part is created.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    #### Methods ##############################################################

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the part.

        The parameter *parent* is the toolkit-specific control that is the
        parts's parent.

        Return the toolkit-specific control.

        """

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the part.

        Return None.

        """

    def set_focus(self):
        """ Set the focus to the appropriate control in the part.

        Return None.

        """


@provides(IWorkbenchPart)
class MWorkbenchPart(HasTraits):
    """ Mixin containing common code for toolkit-specific implementations. """
    #### 'IWorkbenchPart' interface ###########################################

    # The toolkit-specific control that represents the part.
    #
    # The framework sets this to the value returned by 'create_control'.
    control = Any

    # Does the part currently have the focus?
    has_focus = Bool(False)

    # The part's globally unique identifier.
    id = Str

    # The part's name (displayed to the user).
    name = Unicode

    # The current selection within the part.
    selection = List

    # The workbench window that the part is in.
    #
    # The framework sets this when the part is created.
    window = Instance('pyface.workbench.api.WorkbenchWindow')

    #### Methods ##############################################################

    def create_control(self, parent):
        """ Create the toolkit-specific control that represents the part. """

        raise NotImplementedError

    def destroy_control(self):
        """ Destroy the toolkit-specific control that represents the part. """

        raise NotImplementedError

    def set_focus(self):
        """ Set the focus to the appropriate control in the part. """

        raise NotImplementedError

#### EOF ######################################################################
