# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import HasTraits, Int, Tuple

from pyface.i_layout_item import ILayoutItem, Size, SizePolicy
from pyface.i_widget import IWidget


class ILayoutWidget(IWidget, ILayoutItem):
    """ Interface for widgets that can participate in layout.

    Most widgets implement ILayoutWidget, but widgets like top-level windows,
    menus, toolbars, etc. do not.
    """
    pass


class MLayoutWidget(HasTraits):
    """ A mixin for Widgets that can participate in layouts.

    Most widgets implement ILayoutWidget, but widgets like top-level windows,
    menus, toolbars, etc. do not.
    """

    #: The minimum size that the widget can take.
    minimum_size = Size

    #: The maximum size that the widget can take.
    maximum_size = Size

    #: Weight factor used to distribute extra space between widgets.
    stretch = Tuple(Int, Int)

    #: How the widget should behave when more space is available.
    size_policy = Tuple(SizePolicy, SizePolicy)

    def _initialize_control(self):
        """ Initialize the toolkit control. """
        super()._initialize_control()
        self._set_control_minimum_size(self.minimum_size)
        self._set_control_maximum_size(self.maximum_size)
        self._set_control_stretch(self.stretch)
        self._set_control_size_policy(self.size_policy)

    def _add_event_listeners(self):
        """ Add trait observers and toolkit binding. """
        super()._add_event_listeners()
        self.observe(
            self._minimum_size_updated,
            "minimum_size",
            dispatch="ui",
        )
        self.observe(
            self._maximum_size_updated,
            "maximum_size",
            dispatch="ui",
        )
        self.observe(
            self._stretch_updated,
            "stretch",
            dispatch="ui",
        )
        self.observe(
            self._size_policy_updated,
            "size_policy",
            dispatch="ui",
        )

    def _remove_event_listeners(self):
        """ Remove trait observers and toolkit binding. """
        self.observe(
            self._minimum_size_updated,
            "minimum_size",
            dispatch="ui",
            remove=True,
        )
        self.observe(
            self._maximum_size_updated,
            "maximum_size",
            dispatch="ui",
            remove=True,
        )
        self.observe(
            self._stretch_updated,
            "stretch",
            dispatch="ui",
            remove=True,
        )
        self.observe(
            self._size_policy_updated,
            "size_policy",
            dispatch="ui",
            remove=True,
        )
        super()._remove_event_listeners()

    def _minimum_size_updated(self, event):
        """ Trait observer for minimum size. """
        if self.control is not None:
            self._set_control_minimum_size(event.new)

    def _maximum_size_updated(self, event):
        """ Trait observer for maximum size. """
        if self.control is not None:
            self._set_control_maximum_size(event.new)

    def _stretch_updated(self, event):
        """ Trait observer for stretch. """
        if self.control is not None:
            self._set_control_stretch(event.new)

    def _size_policy_updated(self, event):
        """ Trait observer for size policy. """
        if self.control is not None:
            self._set_control_size_policy(event.new)

    def _set_control_minimum_size(self, size):
        """ Set the minimum size of the control.

        Toolkit implementations will need to override this method.
        """
        raise NotImplementedError()

    def _get_control_minimum_size(self):
        """ Get the minimum size of the control.

        Toolkit implementations will need to override this method.
        This method is only used for testing.
        """
        raise NotImplementedError()

    def _set_control_maximum_size(self, size):
        """ Set the maximum size of the control.

        Toolkit implementations will need to override this method.
        """
        raise NotImplementedError()

    def _get_control_maximum_size(self):
        """ Get the maximum size of the control.

        Toolkit implementations will need to override this method.
        This method is only used for testing.
        """
        raise NotImplementedError()

    def _set_control_stretch(self, stretch):
        """ Set the stretch factor of the control.

        Toolkit implementations will need to override this method.
        """
        raise NotImplementedError()

    def _get_control_stretch(self):
        """ Get the stretch factor of the control.

        Toolkit implementations will need to override this method.
        This method is only used for testing.
        """
        raise NotImplementedError()

    def _set_control_size_policy(self, size_policy):
        """ Set the size policy of the control.

        Toolkit implementations will need to override this method.
        """
        raise NotImplementedError()

    def _get_control_size_policy(self):
        """ Get the size policy of the control.

        Toolkit implementations will need to override this method.
        This method is only used for testing.
        """
        raise NotImplementedError()
