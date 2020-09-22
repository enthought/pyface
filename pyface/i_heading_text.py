# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Heading text. """


from traits.api import Int, Interface, Str


from pyface.ui_traits import Image


class IHeadingText(Interface):
    """ Heading text. """

    # 'IHeadingText' interface ---------------------------------------------

    #: Heading level.
    #
    # fixme: Currently we ignore anything but one, but in future we could
    # have different visualizations based on the level.
    level = Int(1)

    #: The heading text.
    text = Str("Default")

    #: The background image.
    image = Image()


class MHeadingText(object):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IHeadingText interface.
    """
