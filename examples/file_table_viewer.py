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
""" A table viewer for local file systems. """


# Standard library imports.
from os import listdir, stat
from os.path import basename, isdir, join
from time import localtime, strftime

# Enthought library imports.
from pyface.api import ImageResource
from pyface.viewer.api import TableColumnProvider, TableContentProvider
from pyface.viewer.api import TableLabelProvider, TableViewer
from traits.api import Instance, Str



class FileTableContentProvider(TableContentProvider):
    """ A table content provider for local file systems. """

    #########################################################################
    # 'TableContentProvider' interface.
    #########################################################################

    def get_elements(self, element):
        """ Returns the label for an element. """

        if isdir(element):
            elements = [
                join(element, filename) for filename in listdir(element)
            ]

        else:
            elements = []

        return elements


class FileTableLabelProvider(TableLabelProvider):
    """ A table label provider for local file systems. """

    # The icon used to represent 'folder' elements.
    FOLDER = ImageResource('closed_folder')

    # The icon used to represent 'document' elements.
    DOCUMENT = ImageResource('document')

    ###########################################################################
    # 'TableLabelProvider' interface.
    ###########################################################################

    def get_image(self, viewer, element, column_index=0):
        """ Returns the filename of the label image for an element. """

        if isdir(element):
            image = self.FOLDER

        else:
            image = self.DOCUMENT

        return image

    def get_text(self, viewer, element, column_index=0):
        """ Returns the label text for an element. """

        details = stat(element)

        if column_index == 0:
            label = basename(element)

        elif column_index == 1:
            label = str(int(details.st_size) / 1000) + ' KB'

        else:
            # Format is: mm/dd/yyyy HH:MM AM eg. '12/31/2004 12:00 PM'
            label = strftime('%m/%d/%Y %I:%M %p', localtime(details.st_mtime))

        return label


class FileTableColumnProvider(TableColumnProvider):
    """ A table column provider for local file systems. """

    ###########################################################################
    # 'object' interface.
    ###########################################################################

    def __init__(self):
        """ Creates a new column provider. """

        # Column labels.
        self._column_labels = ['Name', 'Size', 'Date Modified']

        # The number of columns.
        self.column_count = len(self._column_labels)

        return

    ###########################################################################
    # 'TableColumnProvider' interface.
    ###########################################################################

    def get_label(self, viewer, column_index):
        """ Returns the label for a column. """

        return self._column_labels[column_index]

    def get_alignment(self, viewer, column_index):
        """ Returns the alignment of the column header and cells.

        Returns, 'left', 'right', 'centre' or 'center' ('left' by default).

        """

        if column_index == 1:
            alignment = 'right'

        else:
            alignment = 'left'

        return alignment

class FileTableViewer(TableViewer):
    """ A table viewer for local file systems. """

    #### 'TableViewer' interface ##############################################

    # The column provider.
    column_provider = Instance(FileTableColumnProvider, ())

    # The content provider provides the actual table data.
    content_provider = Instance(FileTableContentProvider, ())

    # The label provider provides, err, the labels for the items in the tree
    # (a label can have text and/or an image).
    label_provider = Instance(FileTableLabelProvider, ())

##### EOF #####################################################################
