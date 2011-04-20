""" A view containing a main walter canvas. """


# Enthought library imports.
from pyface.workbench.api import View, WorkbenchWindow
from traits.api import HasTraits, Instance, Str, on_trait_change
from traitsui.api import View as TraitsView


class DebugViewModel(HasTraits):
    """ The model for the debug view! """

    #### 'Model' interface ####################################################

    active_editor = Str
    active_part   = Str
    active_view   = Str

    window = Instance(WorkbenchWindow)

    ###########################################################################
    # 'Model' interface.
    ###########################################################################

    @on_trait_change(
        'window.active_editor', 'window.active_part', 'window.active_view'
    )
    def refresh(self):
        """ Refresh the model. """

        self.active_editor = self._get_id(self.window.active_editor)
        self.active_part   = self._get_id(self.window.active_part)
        self.active_view   = self._get_id(self.window.active_view)

        return

    def _window_changed(self):
        """ Window changed! """

        self.refresh()

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

    def _get_id(self, obj):
        """ Return the Id of an object. """

        if obj is None:
            id = 'None'

        else:
            id = obj.id

        return id


class DebugView(View):
    """ A view containing a main walter canvas. """

    #### 'IWorkbenchPart' interface ###########################################

    # The part's name (displayed to the user).
    name = 'Debug'

    #### 'DebugView' interface ################################################

    # The model for the debug view!
    model = Instance(DebugViewModel)

    ###########################################################################
    # 'IWorkbenchPart' interface.
    ###########################################################################

    def create_control(self, parent):
        """ Creates the toolkit-specific control that represents the view.

        'parent' is the toolkit-specific control that is the view's parent.

        """

        self.model = DebugViewModel(window=self.window)

        ui = self.model.edit_traits(
            parent = parent,
            kind   = 'subpanel',
            view   =  TraitsView('active_part', 'active_editor', 'active_view')
        )

        return ui.control

#### EOF ######################################################################
