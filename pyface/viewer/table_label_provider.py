# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Base class for all table label providers. """


from .label_provider import LabelProvider


class TableLabelProvider(LabelProvider):
    """ Base class for all table label providers.

    By default an item has no icon, and 'str' is used to generate its label.

    """

    # ------------------------------------------------------------------------
    # 'TableLabelProvider' interface.
    # ------------------------------------------------------------------------

    def get_image(self, viewer, element, column_index=0):
        """ Returns the filename of the label image for an element. """

        return None

    def get_text(self, viewer, element, column_index=0):
        """ Returns the label text for an element. """

        return "%s column %d" % (str(element), column_index)
