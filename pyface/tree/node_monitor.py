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
""" A monitor for appearance and structural changes to a node. """

# Standard library imports.
import logging

# Enthought library imports.
from traits.api import Any, Event, HasTraits

# Local imports.
from .node_event import NodeEvent


# Create a logger for this module.
logger = logging.getLogger(__name__)


class NodeMonitor(HasTraits):
    """ A monitor for appearance and structural changes to a node. """

    #### 'NodeMonitor' interface ##############################################

    # The node that we are monitoring.
    node = Any

    #### Events ####

    # Fired when child nodes in the node that we are monitoring have changed in
    # some way that affects their appearance but NOT their structure.
    nodes_changed = Event(NodeEvent)

    # Fired when child nodes have been inserted into the node that we are
    # monitoring.
    nodes_inserted = Event(NodeEvent)

    # Fired when child nodes have been removed from the node that we are
    # monitoring.
    nodes_removed = Event(NodeEvent)

    # Fired when child nodes have been replaced in the node that we are
    # monitoring.
    nodes_replaced = Event(NodeEvent)

    # Fired when the structure of the node that we are monitoring has changed
    # DRASTICALLY (i.e., we do not have enough information to make individual
    # changes/inserts/removals).
    structure_changed = Event(NodeEvent)


    ###########################################################################
    # 'NodeMonitor' interface.
    ###########################################################################

    #### public methods #######################################################

    def start(self):
        """ Start listening to changes to the node. """

        if self.node.obj is not None:
            self._setup_trait_change_handlers(self.node.obj)

        return


    def stop(self):
        """ Stop listening to changes to the node. """

        if self.node.obj is not None:
            self._setup_trait_change_handlers(self.node.obj, remove=True)

        return

    def fire_nodes_changed(self, children=[]):
        """ Fires the nodes changed event. """

        self.nodes_changed = NodeEvent(node=self.node, children=children)

        return

    def fire_nodes_inserted(self, children, index=-1):
        """ Fires the nodes inserted event.

        If the index is -1 it means the nodes were appended.

        fixme: The tree and model should probably have an 'appended' event.

        """

        self.nodes_inserted = NodeEvent(
            node=self.node, children=children, index=index
        )

        return

    def fire_nodes_removed(self, children):
        """ Fires the nodes removed event. """

        self.nodes_removed = NodeEvent(node=self.node, children=children)

        return

    def fire_nodes_replaced(self, old_children, new_children):
        """ Fires the nodes replaced event. """

        self.nodes_replaced = NodeEvent(
            node=self.node, old_children=old_children, children=new_children
        )

        return

    def fire_structure_changed(self):
        """ Fires the structure changed event. """

        self.structure_changed = NodeEvent(node=self.node)

        return


    #### protected methods ####################################################

    def _setup_trait_change_handlers(self, obj, remove=False):
        """ Add or remove trait change handlers to/from a node. """

        logger.debug('%s trait listeners on (%s) in NodeMonitor (%s)',
            (remove and 'Removing' or 'Adding'), obj, self)

        pass # derived classes should do something here!

        return


#### EOF ######################################################################
