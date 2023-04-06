# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import wx

from traits.api import provides

from pyface.i_layout_item import DEFAULT_SIZE
from pyface.i_layout_widget import ILayoutWidget, MLayoutWidget
from pyface.ui.wx.widget import Widget


#: The special "default" size for Wx Size objects.
WX_DEFAULT_SIZE = -1


@provides(ILayoutWidget)
class LayoutWidget(MLayoutWidget, Widget):
    """ A widget which can participate as part of a layout.

    This is an abstract class, as Widget._create_control needs to be
    implemented at a minimum.
    """

    def _set_control_minimum_size(self, size):
        """ Set the minimum size of the control. """
        wx_size = _size_to_wx_size(size)
        self.control.SetMinSize(wx_size)

    def _get_control_minimum_size(self):
        """ Get the minimum size of the control. """
        wx_size = self.control.GetMinSize()
        return _wx_size_to_size(wx_size)

    def _set_control_maximum_size(self, size):
        """ Set the maximum size of the control. """
        wx_size = _size_to_wx_size(size)
        self.control.SetMaxSize(wx_size)

    def _get_control_maximum_size(self):
        """ Get the maximum size of the control. """
        wx_size = self.control.GetMaxSize()
        return _wx_size_to_size(wx_size)

    def _set_control_stretch(self, size_policy):
        """ Set the stretch factor of the control.

        In Wx the stretch factor is set at layout time and can't be changed
        without removing and adding the widget back into a layout.
        """
        pass

    def _get_control_stretch(self):
        """ Get the stretch factor of the control.

        In Wx the stretch factor is set at layout time and can't be obtained
        from the widget itself.  As a result, this method simply returns the
        current trait value.  This method is only used for testing.
        """
        return self.stretch

    def _set_control_size_policy(self, size_policy):
        """ Set the size policy of the control

        In Wx the size policy is set at layout time and can't be changed
        without removing and adding the widget back into a layout.
        """
        pass

    def _get_control_size_policy(self):
        """ Get the size policy of the control

        In Wx the size policy is set at layout time and can't be obtained from
        the widget itself.  As a result, this method simply returns the
        current trait value.  This method is only used for testing.
        """
        return self.size_policy


def _size_to_wx_size(size):
    """ Convert a size tuple to a wx.Size instance.

    Parameters
    ----------
    size : tuple of (width, height)
        The width and height as a tuple of ints.

    Returns
    -------
    wx_size : wx.Size
        A corresponding wx Size instance.
    """
    return wx.Size(*(
        x if x != DEFAULT_SIZE else WX_DEFAULT_SIZE
        for x in size
    ))


def _wx_size_to_size(wx_size):
    """ Convert a wx.Size instance to a size tuple.

    Parameters
    ----------
    wx_size : wx.Size
        A wx Size instance.

    Returns
    -------
    size : tuple of (width, height)
        The corresponding width and height as a tuple of ints.
    """
    return (wx_size.GetWidth(), wx_size.GetHeight())
