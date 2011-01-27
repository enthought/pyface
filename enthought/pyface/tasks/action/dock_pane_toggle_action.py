# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.traits.api import Bool, Instance, Property, Unicode

# Local imports.
from enthought.pyface.tasks.i_dock_pane import IDockPane


class DockPaneToggleAction(Action):
    """ An Action for toggling the visibily of a dock pane.
    """
    
    #### 'ToggleAction' interface #############################################
    
    dock_pane = Instance(IDockPane)

    #### 'Action' interface ###################################################

    name = Property(Unicode, depends_on='dock_pane.name')
    checked = Property(Bool, depends_on='dock_pane.visible')
    style = 'toggle'
    tooltip = Property(Unicode, depends_on='name')
    visible = Property(Bool, depends_on='dock_pane.closable')

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event=None):
        if self.dock_pane:
            self.dock_pane.visible = not self.dock_pane.visible

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_name(self):
        return self.dock_pane.name

    def _get_checked(self):
        return self.dock_pane.visible

    def _get_tooltip(self):
        return u'Toggles the visibilty of the %s pane.' % self.name

    def _get_visible(self):
        return self.dock_pane.closable
