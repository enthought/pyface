# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Enum, Int, Interface, Tuple

#: Value that indicates the default size values should be used.
DEFAULT_SIZE = -1

#: Trait for sizes of widgets.
Size = Tuple(Int(DEFAULT_SIZE), Int(DEFAULT_SIZE))

#: Trait for size policy values.
SizePolicy = Enum("default", "fixed", "preferred", "expand")


class ILayoutItem(Interface):
    """ An item that can participate in layout. """

    #: The minimum size that the item can take.
    minimum_size = Size

    #: The maximum size that the item can take.
    maximum_size = Size

    #: Weight factor used to distribute extra space between widgets.
    stretch = Tuple(Int, Int)

    #: How the item should behave when more space is available.
    size_policy = Tuple(SizePolicy, SizePolicy)
