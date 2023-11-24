# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply

# ------------------------------------------------------------------------------


from pyface.qt import QtCore, QtGui


from traits.api import Bool, Instance, List, Str, Tuple, provides


from pyface.image_cache import ImageCache
from pyface.action.action_manager import ActionManager
from pyface.action.i_tool_bar_manager import IToolBarManager
from pyface.ui_traits import Orientation


@provides(IToolBarManager)
class ToolBarManager(ActionManager):
    """ A tool bar manager realizes itself in errr, a tool bar control. """

    # 'ToolBarManager' interface -------------------------------------------

    # Is the tool bar enabled?
    enabled = Bool(True)

    # Is the tool bar visible?
    visible = Bool(True)

    # The size of tool images (width, height).
    image_size = Tuple((16, 16))

    # The toolbar name (used to distinguish multiple toolbars).
    name = Str("ToolBar")

    # The orientation of the toolbar.
    orientation = Orientation("horizontal")

    # Should we display the name of each tool bar tool under its image?
    show_tool_names = Bool(True)

    # Should we display the horizontal divider?
    show_divider = Bool(True)

    # Private interface ----------------------------------------------------

    # Cache of tool images (scaled to the appropriate size).
    _image_cache = Instance(ImageCache)

    #: Keep track of all created toolbars in order to properly dispose of them
    _toolbars = List()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, *args, **traits):
        """ Creates a new tool bar manager. """

        # Base class constructor.
        super().__init__(*args, **traits)

        # An image cache to make sure that we only load each image used in the
        # tool bar exactly once.
        self._image_cache = ImageCache(self.image_size[0], self.image_size[1])

        return

    # ------------------------------------------------------------------------
    # 'ToolBarManager' interface.
    # ------------------------------------------------------------------------

    def create_tool_bar(self, parent, controller=None):
        """ Creates a tool bar. """

        # If a controller is required it can either be set as a trait on the
        # tool bar manager (the trait is part of the 'ActionManager' API), or
        # passed in here (if one is passed in here it takes precedence over the
        # trait).
        if controller is None:
            controller = self.controller

        # Create the control.
        tool_bar = _ToolBar(self, parent)
        self._toolbars.append(tool_bar)
        tool_bar.setObjectName(self.id)
        tool_bar.setWindowTitle(self.name)

        if self.show_tool_names:
            tool_bar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        if self.orientation == "horizontal":
            tool_bar.setOrientation(QtCore.Qt.Orientation.Horizontal)
        else:
            tool_bar.setOrientation(QtCore.Qt.Orientation.Vertical)

        # We would normally leave it to the current style to determine the icon
        # size.
        w, h = self.image_size
        tool_bar.setIconSize(QtCore.QSize(w, h))

        # Add all of items in the manager's groups to the tool bar.
        self._qt4_add_tools(parent, tool_bar, controller)

        return tool_bar

    # ------------------------------------------------------------------------
    # 'ActionManager' interface.
    # ------------------------------------------------------------------------

    def destroy(self):
        while self._toolbars:
            toolbar = self._toolbars.pop()
            toolbar.dispose()

        super().destroy()

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _qt4_add_tools(self, parent, tool_bar, controller):
        """ Adds tools for all items in the list of groups. """

        previous_non_empty_group = None
        for group in self.groups:
            if len(group.items) > 0:
                # Is a separator required?
                if previous_non_empty_group is not None and group.separator:
                    separator = tool_bar.addSeparator()
                    group.observe(
                        self._separator_visibility_method(separator), "visible"
                    )

                previous_non_empty_group = group

                # Create a tool bar tool for each item in the group.
                for item in group.items:
                    item.add_to_toolbar(
                        parent,
                        tool_bar,
                        self._image_cache,
                        controller,
                        self.show_tool_names,
                    )

    def _separator_visibility_method(self, separator):
        """ Method to return closure to set visibility of group separators. """
        return lambda event: separator.setVisible(event.new)


class _ToolBar(QtGui.QToolBar):
    """ The toolkit-specific tool bar implementation. """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, tool_bar_manager, parent):
        """ Constructor. """

        QtGui.QToolBar.__init__(self, parent)

        # List of tools
        self.tools = []

        # Listen for changes to the tool bar manager's enablement and
        # visibility.
        self.tool_bar_manager = tool_bar_manager

        self.tool_bar_manager.observe(
            self._on_tool_bar_manager_enabled_changed, "enabled"
        )

        self.tool_bar_manager.observe(
            self._on_tool_bar_manager_visible_changed, "visible"
        )

        return

    def dispose(self):
        self.tool_bar_manager.observe(
            self._on_tool_bar_manager_enabled_changed, "enabled", remove=True
        )
        self.tool_bar_manager.observe(
            self._on_tool_bar_manager_visible_changed, "visible", remove=True
        )
        # Removes event listeners from downstream tools and clears their
        # references
        for item in self.tools:
            item.dispose()

        self.tools = []

    # ------------------------------------------------------------------------
    # Trait change handlers.
    # ------------------------------------------------------------------------

    def _on_tool_bar_manager_enabled_changed(self, event):
        """ Dynamic trait change handler. """

        self.setEnabled(event.new)

    def _on_tool_bar_manager_visible_changed(self, event):
        """ Dynamic trait change handler. """

        self.setVisible(event.new)

        return
