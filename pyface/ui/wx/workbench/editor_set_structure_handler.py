# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" The handler used to restore editors.
"""


import logging


from pyface.dock.api import SetStructureHandler


logger = logging.getLogger(__name__)


class EditorSetStructureHandler(SetStructureHandler):
    """ The handler used to restore editors.

    This is part of the 'dock window' API. It is used to resolve dock control
    Ids when setting the structure of a dock window.

    """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, window_layout, editor_mementos):
        """ Creates a new handler. """

        self.window_layout = window_layout
        self.editor_mementos = editor_mementos

        return

    # ------------------------------------------------------------------------
    # 'SetStructureHandler' interface.
    # ------------------------------------------------------------------------

    def resolve_id(self, id):
        """ Resolves an unresolved dock control id. """

        window_layout = self.window_layout
        window = window_layout.window

        try:
            # Get the memento for the editor with this Id.
            memento = self._get_editor_memento(id)

            # Ask the editor manager to create an editor from the memento.
            editor = window.editor_manager.set_editor_memento(memento)

            # Get the editor's toolkit-specific control.
            #
            # fixme: This is using a 'private' method on the window layout.
            # This may be ok since this structure handler is really part of the
            # layout!
            control = window_layout._wx_get_editor_control(editor)

            # fixme: This is ugly manipulating the editors list from in here!
            window.editors.append(editor)

        except:
            logger.warning("could not restore editor [%s]", id)
            control = None

        return control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _get_editor_memento(self, id):
        """ Return the editor memento for the editor with the specified Id.

        Raises a 'ValueError' if no such memento exists.

        """

        editor_memento = self.editor_mementos.get(id)
        if editor_memento is None:
            raise ValueError("no editor memento with Id %s" % id)

        return editor_memento
