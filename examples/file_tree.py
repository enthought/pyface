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
""" A file system tree. """


# Standard library imports.
from os import listdir
from os.path import basename, isdir, join

# Enthought library imports.
from pyface.api import ImageResource
from pyface.tree.api import Tree, TreeModel
from traits.api import Instance


class FileTreeModel(TreeModel):
    """ A tree model for local file systems. """

    # The image used to represent folders that are NOT expanded.
    CLOSED_FOLDER = ImageResource('closed_folder')

    # The image used to represent folders that ARE expanded.
    OPEN_FOLDER = ImageResource('open_folder')

    # The image used to represent documents (ie. NON-'folder') nodes.
    DOCUMENT = ImageResource('document')

    #########################################################################
    # 'TreeModel' interface.
    #########################################################################

    def get_children(self, node):
        """ Returns the children of a node. """

        return [join(node, filename) for filename in listdir(node)]

    def has_children(self, node):
        """ Returns True if a node has children, otherwise False. """

        if isdir(node):
            has_children = len(listdir(node)) > 0

        else:
            has_children = False

        return has_children

    def get_image(self, node, selected, expanded):
        """ Returns the label image for a node. """

        if isdir(node):
            if expanded:
                image = self.OPEN_FOLDER

            else:
                image = self.CLOSED_FOLDER

        else:
            image = self.DOCUMENT

        return image

    def get_text(self, node):
        """ Returns the label text for a node. """

        return basename(node)


class FileTree(Tree):
    """ A file system tree. """

    #### 'Tree' interface #####################################################

    # The model that provides the data for the tree.
    model = Instance(FileTreeModel, ())

##### EOF #####################################################################
