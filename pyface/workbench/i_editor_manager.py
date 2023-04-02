# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The editor manager interface. """


from traits.api import Instance, Interface


class IEditorManager(Interface):
    """ The editor manager interface. """

    # The workbench window that the editor manager manages editors for ;^)
    window = Instance("pyface.workbench.api.WorkbenchWindow")

    def add_editor(self, editor, kind):
        """ Registers an existing editor. """

    def create_editor(self, window, obj, kind):
        """ Create an editor for an object.

        'kind' optionally contains any data required by the specific editor
        manager implementation to decide what type of editor to create.

        Returns None if no editor can be created for the resource.
        """

    def get_editor(self, window, obj, kind):
        """ Get the editor that is currently editing an object.

        'kind' optionally contains any data required by the specific editor
        manager implementation to decide what type of editor to create.

        Returns None if no such editor exists.
        """

    def get_editor_kind(self, editor):
        """ Return the 'kind' associated with 'editor'. """

    def get_editor_memento(self, editor):
        """ Return the state of an editor suitable for pickling etc.
        """

    def set_editor_memento(self, memento):
        """ Restore an editor from a memento and return it. """
