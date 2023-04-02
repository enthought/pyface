# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The 'null' specific implementations of the action manager internal classes.
"""


from traits.api import Any, Bool, HasTraits


class _MenuItem(HasTraits):
    """ A menu item representation of an action item. """

    # '_MenuItem' interface ------------------------------------------------

    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any()

    # Is the item enabled?
    enabled = Bool(True)

    # Is the item visible?
    visible = Bool(True)

    # The radio group we are part of (None if the menu item is not part of such
    # a group).
    group = Any()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, parent, menu, item, controller):
        """ Creates a new menu item for an action item. """

        self.item = item

        self.control_id = 1
        self.control = None

        if controller is not None:
            self.controller = controller
            controller.add_to_menu(self)


class _Tool(HasTraits):
    """ A tool bar tool representation of an action item. """

    # '_Tool' interface ----------------------------------------------------

    # Is the item checked?
    checked = Bool(False)

    # A controller object we delegate taking actions through (if any).
    controller = Any()

    # Is the item enabled?
    enabled = Bool(True)

    # Is the item visible?
    visible = Bool(True)

    # The radio group we are part of (None if the tool is not part of such a
    # group).
    group = Any()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(
        self, parent, tool_bar, image_cache, item, controller, show_labels
    ):
        """ Creates a new tool bar tool for an action item. """

        self.item = item
        self.tool_bar = tool_bar

        self.control_id = 1
        self.control = None
        if controller is not None:
            self.controller = controller
            controller.add_to_toolbar(self)


class _PaletteTool(HasTraits):
    """ A tool palette representation of an action item. """

    # '_PaletteTool' interface ---------------------------------------------

    # The radio group we are part of (None if the tool is not part of such a
    # group).
    group = Any()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, tool_palette, image_cache, item, show_labels):
        """ Creates a new tool palette tool for an action item. """

        self.item = item
        self.tool_palette = tool_palette
