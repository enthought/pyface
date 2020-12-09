# (C) Copyright 2008-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# -----------------------------------------------------------------------------
# Copyright (c) 2008, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Riverbank Computing Limited
# Description: <Enthought undo package component>
# -----------------------------------------------------------------------------


# Enthought library imports.
from pyface.action.api import Action, Group, MenuManager
from pyface.workbench.api import WorkbenchWindow
from pyface.workbench.action.api import MenuBarManager, ToolBarManager
from traits.api import Instance
from pyface.undo.action.api import CommandAction, RedoAction, UndoAction

# Local imports.
from example_editor_manager import ExampleEditorManager
from commands import LabelIncrementSizeCommand, LabelDecrementSizeCommand, \
    LabelNormalFontCommand, LabelBoldFontCommand, LabelItalicFontCommand


class ExampleUndoWindow(WorkbenchWindow):
    """ The ExampleUndoWindow class is a workbench window that contains example
    editors that demonstrate the use of the undo framework.
    """

    #### Private interface ####################################################

    # The action that exits the application.
    _exit_action = Instance(Action)

    # The File menu.
    _file_menu = Instance(MenuManager)

    # The Label menu.
    _label_menu = Instance(MenuManager)

    # The Undo menu.
    _undo_menu = Instance(MenuManager)

    ###########################################################################
    # Private interface.
    ###########################################################################

    #### Trait initialisers ###################################################

    def __file_menu_default(self):
        """ Trait initialiser. """

        return MenuManager(self._exit_action, name="&File")

    def __undo_menu_default(self):
        """ Trait initialiser. """
        undo_manager = self.workbench.undo_manager

        undo_action = UndoAction(undo_manager=undo_manager)
        redo_action = RedoAction(undo_manager=undo_manager)

        return MenuManager(undo_action, redo_action, name="&Undo")

    def __label_menu_default(self):
        """ Trait initialiser. """

        size_group = Group(CommandAction(command=LabelIncrementSizeCommand),
                           CommandAction(command=LabelDecrementSizeCommand))

        normal = CommandAction(id='normal', command=LabelNormalFontCommand,
                               style='radio', checked=True)
        bold = CommandAction(id='bold', command=LabelBoldFontCommand,
                             style='radio')
        italic = CommandAction(id='italic', command=LabelItalicFontCommand,
                               style='radio')

        style_group = Group(normal, bold, italic, id='style')

        return MenuManager(size_group, style_group, name="&Label")

    def __exit_action_default(self):
        """ Trait initialiser. """

        return Action(name="E&xit", on_perform=self.workbench.exit)

    def _editor_manager_default(self):
        """ Trait initialiser. """

        return ExampleEditorManager()

    def _menu_bar_manager_default(self):
        """ Trait initialiser. """

        return MenuBarManager(
            self._file_menu,
            self._label_menu,
            self._undo_menu,
            window=self
        )

    def _tool_bar_manager_default(self):
        """ Trait initialiser. """

        return ToolBarManager(self._exit_action, show_tool_names=False)

    def _active_editor_changed(self, old, new):
        """ Trait handler. """

        # Tell the undo manager about the new command stack.
        if old is not None:
            old.command_stack.undo_manager.active_stack = None

        if new is not None:
            new.command_stack.undo_manager.active_stack = new.command_stack

        # Walk the label editor menu.
        for grp in self._label_menu.groups:
            for itm in grp.items:
                action = itm.action

                # Enable the action and set the command stack and data if there
                # is a new editor.
                if new is not None:
                    action.enabled = True
                    action.command_stack = new.command_stack
                    action.data = new.obj

                    # FIXME v3: We should just be able to check the menu option
                    # corresponding to the style trait - but that doesn't seem
                    # to uncheck the other options in the group.  Even then the
                    # first switch to another editor doesn't update the menus
                    # (though subsequent ones do).
                    if grp.id == 'style':
                        action.checked = (action.data.style == action.id)
                else:
                    action.enabled = False
