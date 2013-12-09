""" Base class defining common code for EnamlTaskPane and EnamlEditor. """

# Enthought library imports.
from traits.api import HasTraits, Instance


class EnamlPane(HasTraits):
    """ Base class defining common code for EnamlTaskPane and EnamlEditor. """

    ###########################################################################
    # 'EnamlPane' interface
    ###########################################################################

    #: The Enaml component defining the contents of the TaskPane.
    component = Instance('enaml.widgets.toolkit_object.ToolkitObject')

    def create_component(self):
        """ Return an Enaml component defining the contents of the pane.

        Returns
        -------
        component : ToolkitObject
        """
        raise NotImplementedError

    ###########################################################################
    # 'TaskPane'/'Editor' interface
    ###########################################################################

    def create(self, parent):
        """ Create the toolkit-specific control that represents the editor. """

        from enaml.widgets.constraints_widget import ProxyConstraintsWidget

        self.component = self.create_component()

        # We start with an invisible component to avoid flicker. We restore the
        # initial state after the Qt control is parented.
        visible = self.component.visible
        self.component.visible = False

        # Initialize the proxy.
        self.component.initialize()

        # Activate the proxy.
        if not self.component.proxy_is_active:
            self.component.activate_proxy()

        # Fish the Qt control out of the proxy. That's our TaskPane content.
        self.control = self.component.proxy.widget

        # Set the parent
        if parent is not None:
            self.control.setParent(parent)

        # Restore the visibility state
        self.component.visible = visible
        if isinstance(self.component, ProxyConstraintsWidget):
            self.component.proxy.request_relayout()

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the editor.
        """

        control = self.control
        if control is not None:
            control.hide()
            self.component.destroy()
            control.deleteLater()

        self.control = None
        self.component = None
