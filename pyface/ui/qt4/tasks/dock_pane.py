# Standard library imports
from contextlib import contextmanager

# Enthought library imports.
from pyface.tasks.i_dock_pane import IDockPane, MDockPane
from traits.api import Bool, on_trait_change, Property, provides, Tuple

# System library imports.
from pyface.qt import QtCore, QtGui

# Local imports.
from .task_pane import TaskPane
from .util import set_focus

# Constants.
AREA_MAP = { 'left'   : QtCore.Qt.LeftDockWidgetArea,
             'right'  : QtCore.Qt.RightDockWidgetArea,
             'top'    : QtCore.Qt.TopDockWidgetArea,
             'bottom' : QtCore.Qt.BottomDockWidgetArea }
INVERSE_AREA_MAP = dict((int(v), k) for k, v in AREA_MAP.items())


@provides(IDockPane)
class DockPane(TaskPane, MDockPane):
    """ The toolkit-specific implementation of a DockPane.

    See the IDockPane interface for API documentation.
    """

    #### 'IDockPane' interface ################################################

    size = Property(Tuple)

    #### Protected traits #####################################################

    _receiving = Bool(False)

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the dock widget that contains the pane contents.
        """
        self.control = control = QtGui.QDockWidget(parent)

        # Set the widget's object name. This important for QMainWindow state
        # saving. Use the task ID and the pane ID to avoid collisions when a
        # pane is present in multiple tasks attached to the same window.
        control.setObjectName(self.task.id + ':' + self.id)

        # Configure the dock widget according to the DockPane settings.
        self._set_dock_features()
        self._set_dock_title()
        self._set_floating()
        self._set_visible()

        # Connect signal handlers for updating DockPane traits.
        control.dockLocationChanged.connect(self._receive_dock_area)
        control.topLevelChanged.connect(self._receive_floating)
        control.visibilityChanged.connect(self._receive_visible)

        # Add the pane contents to the dock widget.
        contents = self.create_contents(control)
        control.setWidget(contents)

        # For some reason the QDockWidget doesn't respect the minimum size
        # of its widgets
        contents_minsize = contents.minimumSize()
        style = control.style()
        contents_minsize.setHeight(contents_minsize.height()
            + style.pixelMetric(style.PM_DockWidgetHandleExtent))
        control.setMinimumSize(contents_minsize)

        # Hide the control by default. Otherwise, the widget will visible in its
        # parent immediately!
        control.hide()

    def set_focus(self):
        """ Gives focus to the control that represents the pane.
        """
        if self.control is not None:
            set_focus(self.control.widget())

    ###########################################################################
    # 'IDockPane' interface.
    ###########################################################################

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        return QtGui.QWidget(parent)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    @contextmanager
    def _signal_context(self):
        """ Defines a context appropriate for Qt signal callbacks. Necessary to
            prevent feedback between Traits and Qt event handlers.
        """
        original = self._receiving
        self._receiving = True
        yield
        self._receiving = original

    #### Trait property getters/setters #######################################

    def _get_size(self):
        if self.control is not None:
            return (self.control.width(), self.control.height())
        return (-1, -1)

    #### Trait change handlers ################################################

    @on_trait_change('dock_area')
    def _set_dock_area(self):
        if self.control is not None and not self._receiving:
            # Only attempt to adjust the area if the task is active.
            main_window = self.task.window.control
            if main_window and self.task == self.task.window.active_task:
                # Qt will automatically remove the dock widget from its previous
                # area, if it had one.
                main_window.addDockWidget(AREA_MAP[self.dock_area],
                                          self.control)

    @on_trait_change('closable,floatable,movable')
    def _set_dock_features(self):
        if self.control is not None:
            features = QtGui.QDockWidget.NoDockWidgetFeatures
            if self.closable:
                features |= QtGui.QDockWidget.DockWidgetClosable
            if self.floatable:
                features |= QtGui.QDockWidget.DockWidgetFloatable
            if self.movable:
                features |= QtGui.QDockWidget.DockWidgetMovable
            self.control.setFeatures(features)

    @on_trait_change('name')
    def _set_dock_title(self):
        if self.control is not None:
            self.control.setWindowTitle(self.name)

    @on_trait_change('floating')
    def _set_floating(self):
        if self.control is not None and not self._receiving:
            self.control.setFloating(self.floating)

    @on_trait_change('visible')
    def _set_visible(self):
        if self.control is not None and not self._receiving:
            self.control.setVisible(self.visible)

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
