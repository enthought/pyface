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
""" The node manager looks after a collection of node types. """

# Standard library imports.
import logging

# Enthought library imports.
from traits.api import HasPrivateTraits, List

# Local imports
from .node_type import NodeType


# Create a logger for this module.
logger = logging.getLogger(__name__)


class NodeManager(HasPrivateTraits):
    """ The node manager looks after a collection of node types. """

    #### 'NodeManager' interface ##########################################

    # All registered node types.
    node_types = List(NodeType)

    # fixme: Where should the system actions go?  The node tree, the node
    # tree model, here?!?
    system_actions = List

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self, **traits):
        """ Creates a new tree model. """

        # Base class constructor.
        super(NodeManager, self).__init__(**traits)

        # This saves looking up a node's type every time.  If we ever have
        # nodes that change type dynamically then we will obviously have to
        # re-think this (although we should probably re-think dynamic type
        # changes first ;^).
        self._node_to_type_map = {} # { Any node : NodeType node_type }

        return

    ###########################################################################
    # 'NodeManager' interface.
    ###########################################################################

    # fixme: This is the only API call that we currently have that manipulates
    # the manager's node types.  Should we make the 'node_types' list
    # available via the public API?
    def add_node_type(self, node_type):
        """ Adds a new node type to the manager. """

        node_type.node_manager = self
        self.node_types.append(node_type)

        return

    def get_node_type(self, node):
        """ Returns the node's type.

        Returns None if none of the manager's node types recognize the node.

        """

        # Generate the key for the node to type map.
        key = self.get_key(node)

        # Check the cache first.
        node_type = self._node_to_type_map.get(key, None)
        if node_type is None:
            # If we haven't seen this node before then attempt to find a node
            # type that 'recognizes' it.
            #
            # fixme: We currently take the first node type that recognizes the
            # node.  This obviously means that ordering of node types is
            # important,  but we don't have an interface for controlling the
            # order.  Maybe sort on some 'precedence' trait on the node type?
            for node_type in self.node_types:
                if node_type.is_type_for(node):
                    self._node_to_type_map[key] = node_type
                    break

            else:
                node_type = None

        if node_type is None:
            logger.warn('no node type for %s' % str(node))

        return node_type

    def get_key(self, node):
        """ Generates a unique key for a node.

        In this case,  'unique' means unqiue within the node manager.

        """

        # We do it like this 'cos, for example, using id() on a string doesn't
        # give us what we want, but things like lists aren't hashable, so we
        # can't always use hash()).
        try:
            key = hash(node)

        except:
            key = id(node)

        return key

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _node_types_changed(self, new):
        """ Called when the entire list of node types has been changed. """

        for node_type in new:
            node_type.node_manager = self

        return

#### EOF ######################################################################
