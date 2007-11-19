""" An action that shows a dialog to allow the user to choose a view. """


# Local imports.
from show_view import ViewChooser
from workbench_action import WorkbenchAction


class ShowViewAction(WorkbenchAction):
    """ An action that shows a dialog to allow the user to choose a view. """

    #### 'Action' interface ###################################################

    # The action's unique identifier (may be None).
    id = 'enthought.pyface.workbench.action.show_other_view'

    # The action's name (displayed on menus/tool bar tools etc).
    name = 'Other...'
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event):
        """ Perform the action. """

        chooser = ViewChooser(window=event.window)
        
        ui = chooser.edit_traits(parent=event.window.control, kind='livemodal')
        if ui.result:
            chooser.view.show()
            chooser.view.set_focus()
            
        return

#### EOF ######################################################################
