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
""" Base class for all tree label providers. """


# Local imports.
from .label_provider import LabelProvider


class TreeLabelProvider(LabelProvider):
    """ Base class for all tree label providers.

    By default an element has no label image, and 'str' is used to generate its
    label text.

    """

    ###########################################################################
    # 'LabelProvider' interface.
    ###########################################################################

    def set_text(self, viewer, element, text):
        """ Sets the text representation of a node.

        Returns True if setting the text succeeded, otherwise False.

        """

        return len(text.strip()) > 0

    ###########################################################################
    # 'TreeLabelProvider' interface.
    ###########################################################################

    def get_drag_value(self, viewer, element):
        """ Get the value that is dragged for an element.

        By default the drag value is the element itself.

        """

        return element

    def is_collapsible(self, viewer, element):
        """ Returns True is the element is collapsible, otherwise False. """

        return True

    def is_expandable(self, viewer, node):
        """ Returns True is the node is expandanble, otherwise False. """

        return True

#### EOF ######################################################################
