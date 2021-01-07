# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A file system tree. """


from os import listdir
from os.path import basename, isdir, isfile, join


from pyface.tree.api import NodeManager, NodeType


class FileNode(NodeType):
    """ Node type for files. """

    # ------------------------------------------------------------------------
    # 'NodeType' interface.
    # ------------------------------------------------------------------------

    def is_type_for(self, node):
        """ Returns True if this node type recognizes a node. """

        return isfile(node)

    def allows_children(self, node):
        """ Does the node allow children (ie. a folder vs a file). """

        return False

    def get_text(self, node):
        """ Returns the label text for a node. """

        return basename(node)


class FolderNode(NodeType):
    """ Node type for folders. """

    # ------------------------------------------------------------------------
    # 'NodeType' interface.
    # ------------------------------------------------------------------------

    def is_type_for(self, node):
        """ Returns True if this node type recognizes a node. """

        return isdir(node)

    def allows_children(self, node):
        """ Does the node allow children (ie. a folder vs a file). """

        return True

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False. """

        return len(listdir(node)) > 0

    def get_children(self, node):
        """ Returns the children of a node. """

        return [join(node, filename) for filename in listdir(node)]

    def get_text(self, node):
        """ Returns the label text for a node. """

        return basename(node)


# Add all types to the node manager.
node_manager = NodeManager()
node_manager.add_node_type(FileNode())
node_manager.add_node_type(FolderNode())
