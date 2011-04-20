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
""" Abstract base class for a node in a preference dialog.

A preference node has a label and an image which are used to represent the node
in a preference dialog (usually in the form of a tree).

"""


# Enthought library imports.
from pyface.viewer.tree_item import TreeItem
from traits.api import Str


class PreferenceNode(TreeItem):
    """ Abstract base class for a node in a preference dialog.

    A preference node has a name and an image which are used to represent the
    node in a preference dialog (usually in the form of a tree).

    """

    #### 'PreferenceNode' interface ###########################################

    # The node's unique Id.
    id = Str

    # The node's image.
    image = Str

    # The node name.
    name = Str

    # The Id of the help topic for the node.
    help_id = Str

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __str__(self):
        """ Returns the string representation of the item. """

        return self.name

    ###########################################################################
    # 'PreferenceNode' interface.
    ###########################################################################

    def create_page(self):
        """ Creates the preference page for this node. """

        raise NotImplementedError

    def lookup(self, id):
        """ Returns the child of this node with the specified Id.

        Returns None if no such child exists.

        """

        for node in self.children:
            if node.id == id:
                break

        else:
            node = None

        return node

#### EOF ######################################################################
