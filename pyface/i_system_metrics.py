# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface to system metrics (screen width and height etc). """


from traits.api import HasTraits, Int, Interface, List, Tuple


class ISystemMetrics(Interface):
    """ The interface to system metrics (screen width and height etc). """

    # 'ISystemMetrics' interface -------------------------------------------

    #: The width of the main screen in pixels.
    screen_width = Int()

    #: The height of the main screen in pixels.
    screen_height = Int()

    #: The height and width of each screen in pixels
    screen_sizes = List(Tuple(Int, Int))

    #: Background color of a standard dialog window as a tuple of RGB values
    #: between 0.0 and 1.0.
    # FIXME v3: Why isn't this a traits colour?
    dialog_background_color = Tuple()


class MSystemMetrics(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the ISystemMetrics interface.
    """
