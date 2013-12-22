# Standard library imports
from contextlib import contextmanager

# Enthought library imports.
from pyface.tasks.i_dock_pane import IDockPane, MDockPane
from traits.api import Bool, on_trait_change, Property, provides, Tuple, Str

# System library imports.
import wx
from pyface.wx.aui import aui

# Local imports.
from task_pane import TaskPane
from util import set_focus

# Constants.
AREA_MAP = { 'left'   : aui.AUI_DOCK_LEFT,
             'right'  : aui.AUI_DOCK_RIGHT,
             'top'    : aui.AUI_DOCK_TOP,
             'bottom' : aui.AUI_DOCK_BOTTOM }
INVERSE_AREA_MAP = dict((int(v), k) for k, v in AREA_MAP.iteritems())


@provides(IDockPane)
class DockPane(TaskPane, MDockPane):
    """ The toolkit-specific implementation of a DockPane.

    See the IDockPane interface for API documentation.
    """
    
    # Keep a reference to the Aui pane name in order to update dock state
    pane_name = Str
    
    #### 'IDockPane' interface ################################################

    size = Property(Tuple)

    #### Protected traits #####################################################

    _receiving = Bool(False)

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    @classmethod
    def print_hierarchy(cls, parent, indent=""):
        print "%s%s %s" % (indent, str(parent), parent.GetName())
        for child in parent.GetChildren():
            cls.print_hierarchy(child, indent + "  ")

    def create(self, parent):
        """ Create and set the dock widget that contains the pane contents.
        """
        # wx doesn't need a wrapper control, so the contents become the control
        self.control = self.create_contents(parent)

        # Set the widget's object name. This important for AUI Manager state
        # saving. Use the task ID and the pane ID to avoid collisions when a
        # pane is present in multiple tasks attached to the same window.
        self.pane_name = self.task.id + ':' + self.id
        print "WX: dock_pane.create: %s" % self.pane_name
        
        self.print_hierarchy(parent)
        # Connect signal handlers for updating DockPane traits.
#        control.dockLocationChanged.connect(self._receive_dock_area)
#        control.topLevelChanged.connect(self._receive_floating)
#        control.visibilityChanged.connect(self._receive_visible)
    
    def get_info(self):
        info = aui.AuiPaneInfo().Name(self.pane_name).DestroyOnClose(False)

        # size?

        # Configure the dock widget according to the DockPane settings.
        self.update_dock_features(info)
        self.update_dock_title(info)
        self.update_floating(info)
        #self.update_visible(info)
        
        info.Hide()
        info.Show(False)
        
        return info
    
    def add_to_manager(self):
        info = self.get_info()
        self.task.window._aui_manager.AddPane(self.control, info)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the contents.
        """
        if self.control is not None:
            print "Destroying %s" % self.control
            self.task.window._aui_manager.DetachPane(self.control)
            self.control.Hide()
            self.control.Destroy()
            self.control = None

    ###########################################################################
    # 'IDockPane' interface.
    ###########################################################################

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        return wx.Window(parent, name=self.task.id + ':' + self.id)

#    ###########################################################################
#    # Protected interface.
#    ###########################################################################
#
#    @contextmanager
#    def _signal_context(self):
#        """ Defines a context appropriate for Qt signal callbacks. Necessary to
#            prevent feedback between Traits and Qt event handlers.
#        """
#        original = self._receiving
#        self._receiving = True
#        yield
#        self._receiving = original

    #### Trait property getters/setters #######################################

    def _get_size(self):
        if self.control is not None:
            return self.control.GetSizeTuple()
        return (-1, -1)

    #### Trait change handlers ################################################

    def get_pane_info(self):
        info = self.task.window._aui_manager.GetPane(self.pane_name)
        return info
    
    def commit_layout(self):
        self.task.window._aui_manager.Update()

    def commit_if_active(self):
        # Only attempt to commit the AUI changes if the area if the task is active.
        main_window = self.task.window.control
        if main_window and self.task == self.task.window.active_task:
            self.commit_layout()
        else:
            print "task not active so not committing..."

    def update_dock_area(self, info):
        info.Direction(AREA_MAP[self.dock_area])
        print "info: dock_area=%s dir=%s" % (self.dock_area, info.dock_direction)

    @on_trait_change('dock_area')
    def _set_dock_area(self):
        print "trait change: dock_area"
        if self.control is not None:
            info = self.get_pane_info()
            self.update_dock_area(info)
            self.commit_if_active()

    def update_dock_features(self, info):
        info.CloseButton(self.closable)
        info.Floatable(self.floatable)
        info.Movable(self.movable)

    @on_trait_change('closable', 'floatable', 'movable')
    def _set_dock_features(self):
        if self.control is not None:
            info = self.get_pane_info()
            self.update_dock_features(info)
            self.commit_if_active()

    def update_dock_title(self, info):
        info.Caption(self.name)

    @on_trait_change('name')
    def _set_dock_title(self):
        if self.control is not None:
            info = self.get_pane_info()
            self.update_dock_title(info)
            self.commit_if_active()

    def update_floating(self, info):
        if self.floating:
            info.Float()
        else:
            info.Dock()

    @on_trait_change('floating')
    def _set_floating(self):
        if self.control is not None:
            info = self.get_pane_info()
            self.update_floating(info)
            self.commit_if_active()

    def update_visible(self, info):
        if self.visible:
            info.Show()
        else:
            info.Hide()

    @on_trait_change('visible')
    def _set_visible(self):
        if self.control is not None:
            print "WX: _set_visible on %s" % self.control.GetName()
            info = self.get_pane_info()
            self.update_visible(info)
            self.commit_if_active()

    #### Signal handlers ######################################################

    def _receive_dock_area(self, area):
        with self._signal_context():
            self.dock_area = INVERSE_AREA_MAP[int(area)]

    def _receive_floating(self, floating):
        with self._signal_context():
            self.floating = floating

    def _receive_visible(self):
        with self._signal_context():
            if self.control is not None:
                self.visible = self.control.isVisible()
