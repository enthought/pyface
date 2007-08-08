""" A view containing a main walter canvas. """


# Enthought library imports.
from enthought.etsconfig.api import ETSConfig
from enthought.traits.api import HasTraits, Instance, Str, on_trait_change

# Local imports.
from view import View
from workbench_window import WorkbenchWindow


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

        method = getattr(self, '_create_control_%s' % ETSConfig.toolkit)
        if method is None:
            raise SystemError('Unknown toolkit %s' % ETSConfig.toolkit)

        return method(parent)

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### wx ###################################################################

    def _create_control_wx(self, parent):
        """ Creates the wx control that represents the view. """

        from enthought.traits.ui.api import View

        ui = self.model.edit_traits(
            parent = parent,
            kind   = 'subpanel',
            view   =  View('active_part', 'active_editor', 'active_view')
        )

        return ui.control

    #### qt4 ##################################################################

    def _create_control_qt4(self, parent):
        """ Creates the qt4 control that represents the view. """

        from PyQt4 import QtGui

        layout = QtGui.QGridLayout()

        layout.addWidget(QtGui.QLabel("Active Part"), 0, 0)
        self._active_part_widget = QtGui.QLineEdit()
        layout.addWidget(self._active_part_widget, 0, 1)
        
        layout.addWidget(QtGui.QLabel("Active Editor"), 1, 0)
        self._active_editor_widget = QtGui.QLineEdit()
        layout.addWidget(self._active_editor_widget, 1, 1)

        layout.addWidget(QtGui.QLabel("Active View"), 2, 0)
        self._active_view_widget = QtGui.QLineEdit()
        layout.addWidget(self._active_view_widget, 2, 1)
        
        layout.setRowStretch(3, 1)

        ui = QtGui.QWidget(parent)
        ui.setLayout(layout)

        # Make sure the widgets reflect the state of the model.
        self._refresh()

        # Listen for changes to the model.
        self.model.on_trait_change(self._on_model_anytrait_changed)
        
        return ui

    def _on_model_anytrait_changed(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        if self.control is not None:
            self._refresh()

        return
    
    def _refresh(self):
        """  Make sure the widgets reflect the state of the model. """

        self._active_part_widget.setText(str(self.model.active_part))
        self._active_editor_widget.setText(str(self.model.active_editor))
        self._active_view_widget.setText(str(self.model.active_view))
            
        return
    
#### EOF ######################################################################
