# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from contextlib import contextmanager


from pyface.tasks.i_dock_pane import IDockPane, MDockPane
from traits.api import Bool, observe, Property, provides, Tuple


from pyface.qt import QtCore, QtGui


from .task_pane import TaskPane
from .util import set_focus

# Constants.
AREA_MAP = {
    "left": QtCore.Qt.DockWidgetArea.LeftDockWidgetArea,
    "right": QtCore.Qt.DockWidgetArea.RightDockWidgetArea,
    "top": QtCore.Qt.DockWidgetArea.TopDockWidgetArea,
    "bottom": QtCore.Qt.DockWidgetArea.BottomDockWidgetArea,
}
INVERSE_AREA_MAP = {v: k for k, v in AREA_MAP.items()}


@provides(IDockPane)
class DockPane(TaskPane, MDockPane):
    """ The toolkit-specific implementation of a DockPane.

    See the IDockPane interface for API documentation.
    """

    # 'IDockPane' interface ------------------------------------------------

    size = Property(Tuple)

    # Protected traits -----------------------------------------------------

    _receiving = Bool(False)

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def create(self, parent):
        """ Create and set the dock widget that contains the pane contents.
        """
        self.control = control = QtGui.QDockWidget(parent)

        # Set the widget's object name. This important for QMainWindow state
        # saving. Use the task ID and the pane ID to avoid collisions when a
        # pane is present in multiple tasks attached to the same window.
        control.setObjectName(self.task.id + ":" + self.id)

        # Ensure that undocked ("floating") windows are visible on macOS
        # when focus is switched, for consistency with Linux and Windows.
        control.setAttribute(QtCore.Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow)

        # Configure the dock widget according to the DockPane settings.
        self._set_dock_features(event=None)
        self._set_dock_title(event=None)
        self._set_floating(event=None)
        self._set_visible(event=None)

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
        contents_minsize.setHeight(
            contents_minsize.height()
            + style.pixelMetric(style.PixelMetric.PM_DockWidgetHandleExtent)
        )
        control.setMinimumSize(contents_minsize)

        # Hide the control by default. Otherwise, the widget will visible in its
        # parent immediately!
        control.hide()

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        if self.control is not None:
            control = self.control
            control.dockLocationChanged.disconnect(self._receive_dock_area)
            control.topLevelChanged.disconnect(self._receive_floating)
            control.visibilityChanged.disconnect(self._receive_visible)

        super().destroy()

    def set_focus(self):
        """ Gives focus to the control that represents the pane.
        """
        if self.control is not None:
            set_focus(self.control.widget())

    # ------------------------------------------------------------------------
    # 'IDockPane' interface.
    # ------------------------------------------------------------------------

    def create_contents(self, parent):
        """ Create and return the toolkit-specific contents of the dock pane.
        """
        return QtGui.QWidget(parent)

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    @contextmanager
    def _signal_context(self):
        """ Defines a context appropriate for Qt signal callbacks. Necessary to
            prevent feedback between Traits and Qt event handlers.
        """
        original = self._receiving
        self._receiving = True
        yield
        self._receiving = original

    # Trait property getters/setters ---------------------------------------

    def _get_size(self):
        if self.control is not None:
            return (self.control.width(), self.control.height())
        return (-1, -1)

    # Trait change handlers ------------------------------------------------

    @observe("dock_area")
    def _set_dock_area(self, event):
        if self.control is not None and not self._receiving:
            # Only attempt to adjust the area if the task is active.
            main_window = self.task.window.control
            if main_window and self.task == self.task.window.active_task:
                # Qt will automatically remove the dock widget from its previous
                # area, if it had one.
                main_window.addDockWidget(
                    AREA_MAP[self.dock_area], self.control
                )

    @observe("closable,floatable,movable")
    def _set_dock_features(self, event):
        if self.control is not None:
            features = QtGui.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures
            if self.closable:
                features |= QtGui.QDockWidget.DockWidgetFeature.DockWidgetClosable
            if self.floatable:
                features |= QtGui.QDockWidget.DockWidgetFeature.DockWidgetFloatable
            if self.movable:
                features |= QtGui.QDockWidget.DockWidgetFeature.DockWidgetMovable
            self.control.setFeatures(features)

    @observe("name")
    def _set_dock_title(self, event):
        if self.control is not None:
            self.control.setWindowTitle(self.name)

    @observe("floating")
    def _set_floating(self, event):
        if self.control is not None and not self._receiving:
            self.control.setFloating(self.floating)

    @observe("visible")
    def _set_visible(self, event):
        if self.control is not None and not self._receiving:
            self.control.setVisible(self.visible)

    # Signal handlers -----------------------------------------------------#

    def _receive_dock_area(self, area):
        with self._signal_context():
            if area in INVERSE_AREA_MAP:
                self.dock_area = INVERSE_AREA_MAP[area]

    def _receive_floating(self, floating):
        with self._signal_context():
            self.floating = floating

    def _receive_visible(self):
        with self._signal_context():
            if self.control is not None:
                self.visible = self.control.isVisible()
