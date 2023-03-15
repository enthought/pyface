# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from enum import Enum

from traits.api import provides

from pyface.qt import QtGui
from pyface.i_layout_item import DEFAULT_SIZE
from pyface.i_layout_widget import ILayoutWidget, MLayoutWidget
from pyface.ui.qt.widget import Widget


#: Maximum widget size (some versions of PyQt don't export it)
QWIDGETSIZE_MAX = getattr(QtGui, "QWIDGETSIZE_MAX", 1 << 24 - 1)


class SizePolicies(Enum):
    """ Qt values for size policies

    Note that Qt has additional values that are not mapped to Pyface size
    policies.
    """
    fixed = QtGui.QSizePolicy.Policy.Fixed
    preferred = QtGui.QSizePolicy.Policy.Preferred
    expand = QtGui.QSizePolicy.Policy.Expanding


@provides(ILayoutWidget)
class LayoutWidget(MLayoutWidget, Widget):
    """ A widget which can participate as part of a layout. """

    def _set_control_minimum_size(self, size):
        size = tuple(
            x if x != DEFAULT_SIZE else 0
            for x in size
        )
        self.control.setMinimumSize(*size)

    def _get_control_minimum_size(self):
        size = self.control.minimumSize()
        return (size.width(), size.height())

    def _set_control_maximum_size(self, size):
        size = tuple(
            x if x != DEFAULT_SIZE else QWIDGETSIZE_MAX
            for x in size
        )
        self.control.setMaximumSize(*size)

    def _get_control_maximum_size(self):
        size = self.control.maximumSize()
        return (size.width(), size.height())

    def _set_control_stretch(self, stretch):
        """ Set the stretch factor of the control.
        """
        new_size_policy = _clone_size_policy(self.control.sizePolicy())
        new_size_policy.setHorizontalStretch(stretch[0])
        new_size_policy.setVerticalStretch(stretch[1])
        self.control.setSizePolicy(new_size_policy)

    def _get_control_stretch(self):
        """ Get the stretch factor of the control.

        This method is only used for testing.
        """
        size_policy = self.control.sizePolicy()
        return (
            size_policy.horizontalStretch(),
            size_policy.verticalStretch(),
        )

    def _set_control_size_policy(self, size_policy):
        new_size_policy = _clone_size_policy(self.control.sizePolicy())
        if size_policy[0] != "default":
            new_size_policy.setHorizontalPolicy(
                SizePolicies[size_policy[0]].value
            )
        if size_policy[1] != "default":
            new_size_policy.setVerticalPolicy(
                SizePolicies[size_policy[1]].value
            )
        self.control.setSizePolicy(new_size_policy)

    def _get_control_size_policy(self):
        size_policy = self.control.sizePolicy()
        if self.size_policy[0] != "default":
            horizontal_policy = SizePolicies(
                size_policy.horizontalPolicy()).name
        else:
            horizontal_policy = "default"
        if self.size_policy[1] != "default":
            vertical_policy = SizePolicies(
                size_policy.verticalPolicy()).name
        else:
            vertical_policy = "default"
        return (horizontal_policy, vertical_policy)

    def destroy(self):
        if self.control is not None:
            self.control.hide()
            super().destroy()


def _clone_size_policy(size_policy):
    """ Clone the state of an existing QSizePolicy object

    This is required because there is no standard Qt copy or clone
    method.
    """
    new_size_policy = QtGui.QSizePolicy()
    new_size_policy.setHorizontalPolicy(
        size_policy.horizontalPolicy()
    )
    new_size_policy.setVerticalPolicy(
        size_policy.verticalPolicy()
    )
    new_size_policy.setHorizontalStretch(
        size_policy.horizontalStretch()
    )
    new_size_policy.setVerticalStretch(
        size_policy.verticalStretch()
    )
    new_size_policy.setHeightForWidth(
        size_policy.hasHeightForWidth()
    )
    new_size_policy.setWidthForHeight(
        size_policy.hasWidthForHeight()
    )
    return new_size_policy
