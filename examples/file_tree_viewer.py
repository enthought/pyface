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
""" A tree viewer for local file systems. """


# Standard library imports.
from os import listdir
from os.path import basename, dirname, isdir, join

# Enthought library imports.
from pyface.api import ImageResource
from pyface.viewer.api import TreeContentProvider, TreeLabelProvider
from pyface.viewer.api import TreeViewer
from traits.api import Instance


class FileTreeContentProvider(TreeContentProvider):
    """ A tree content provider for local file systems. """

    #########################################################################
    # 'TreeContentProvider' interface.
    #########################################################################

    def get_parent(self, element):
        """ Returns the parent of an element. """

        return dirname(element)

    def get_children(self, element):
        """ Returns the children of an element. """

        return [join(element, filename) for filename in listdir(element)]

    def has_children(self, element):
        """ Returns True iff the element has children, otherwise False. """

        if isdir(element):
            for filename in listdir(element):
                if isdir(join(element, filename)):
                    has_children = True
                    break

            else:
                has_children = False
        else:
            has_children = False

        return has_children


class FileTreeLabelProvider(TreeLabelProvider):
    """ A tree label provider for local file systems. """

    # The image used to represent folders that are NOT expanded.
    CLOSED_FOLDER = ImageResource('closed_folder')

    # The image used to represent folders that ARE expanded.
    OPEN_FOLDER = ImageResource('open_folder')

    # The image used to represent documents (ie. NON-'folder') elements.
    DOCUMENT = ImageResource('document')

    ###########################################################################
    # 'TreeLabelProvider' interface.
    ###########################################################################

    def get_image(self, viewer, element):
        """ Returns the filename of the label image for an element. """

        selected = viewer.is_selected(element)
        expanded = viewer.is_expanded(element)

        if isdir(element):
            if expanded:
                image = self.OPEN_FOLDER

            else:
                image = self.CLOSED_FOLDER

        else:
            image = self.DOCUMENT

        return image

    def get_text(self, viewer, element):
        """ Returns the label text for an element. """

        return basename(element)


class FileTreeViewer(TreeViewer):
    """ A tree viewer for local file systems. """

    #### 'TreeViewer' interface ###############################################

    # The content provider provides the actual tree data.
    content_provider = Instance(FileTreeContentProvider, ())

    # The label provider provides, err, the labels for the items in the tree
    # (a label can have text and/or an image).
    label_provider = Instance(FileTreeLabelProvider, ())

##### EOF #####################################################################
