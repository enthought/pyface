# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for all viewers. """


from pyface.layout_widget import LayoutWidget


class Viewer(LayoutWidget):
    """ Abstract base class for all viewers.

    A viewer is a model-based adapter on some underlying toolkit-specific
    widget.

    """

    pass
