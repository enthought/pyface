# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from traits.api import Any, Bool, HasTraits, provides


from pyface.i_widget import IWidget, MWidget


@provides(IWidget)
class Widget(MWidget, HasTraits):
    """ The toolkit specific implementation of a Widget.  See the IWidget
    interface for the API documentation.
    """

    # 'IWidget' interface -------------------------------------------------#

    control = Any()

    parent = Any()

    #: Whether or not the control is visible
    visible = Bool(True)

    #: Whether or not the control is enabled
    enabled = Bool(True)
    # ------------------------------------------------------------------------
    # 'IWidget' interface.
    # ------------------------------------------------------------------------

    def show(self, visible):
        pass

    def enable(self, enabled):
        pass

    def destroy(self):
        self.control = None
