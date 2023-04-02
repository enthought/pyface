# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance


from pyface.tasks.dock_pane import DockPane


class EnamlDockPane(DockPane):
    """ Create a Dock pane for Enaml Components. """

    # ------------------------------------------------------------------------
    # 'EnamlDockPane' interface
    # ------------------------------------------------------------------------

    #: The Enaml component defining the contents of the DockPane.
    component = Instance("enaml.widgets.toolkit_object.ToolkitObject")

    def create_component(self):
        """ Return an Enaml component defining the contents of the DockPane.

        Returns
        -------
        component : ToolkitObject
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------
    # 'IDockPane' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        """ Return the toolkit-specific control that represents the pane. """

        self.component = self.create_component()

        # Initialize the proxy.
        self.component.initialize()

        # Activate the proxy.
        if not self.component.proxy_is_active:
            self.component.activate_proxy()

        # Fish the Qt control out of the proxy. That's our DockPane content.
        contents = self.component.proxy.widget

        return contents

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane. """

        control = self.control
        if control is not None:
            control.hide()
            self.component.destroy()
            control.setParent(None)
            control.deleteLater()

        self.control = None
        self.component = None
