# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for label providers. """


from traits.api import HasTraits


class LabelProvider(HasTraits):
    """ Abstract base class for label providers.

    By default an element has no label image, and 'str' is used to generate its
    label text.

    """

    # ------------------------------------------------------------------------
    # 'LabelProvider' interface.
    # ------------------------------------------------------------------------

    def get_image(self, viewer, element):
        """ Returns the label image for an element. """

        return None

    def get_text(self, viewer, element):
        """ Returns the label text for an element. """

        return str(element)

    def set_text(self, tree, element, text):
        """ Sets the text representation of a node.

        Returns True if setting the text succeeded, otherwise False.

        """

        return True

    def is_editable(self, viewer, element):
        """ Can the label text be changed via the viewer? """

        return False
