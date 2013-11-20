# Enthought library imports.
from traits.api import Instance
from enaml.widgets.toolkit_object import ToolkitObject

# Local imports.
from pyface.tasks.task_pane import TaskPane


class EnamlTaskPane(TaskPane):
    """ Create a Task pane for Enaml Components. """

    ###########################################################################
    # 'EnamlTaskPane' interface
    ###########################################################################

    #: The Enaml component defining the contents of the TaskPane.
    component = Instance(ToolkitObject)

    def create_component(self):
        """ Return an Enaml component defining the contents of the TaskPane.

        Returns
        -------
        component : ToolkitObject
        """
        raise NotImplementedError

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create the toolkit-specific control that represents the pane. """

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
        self.component.proxy.relayout()

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane. """

        control = self.control
        if control is not None:
            control.hide()
            self.component.destroy()
            control.setParent(None)
            control.deleteLater()

        self.control = None
