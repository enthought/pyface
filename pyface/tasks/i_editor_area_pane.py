# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import logging


from traits.api import (
    Bool,
    Callable,
    Dict,
    Event,
    File,
    HasTraits,
    Instance,
    List,
    Str,
)


from pyface.tasks.i_editor import IEditor
from pyface.tasks.i_task_pane import ITaskPane

# Logger.
logger = logging.getLogger(__name__)


class IEditorAreaPane(ITaskPane):
    """ A central pane that contains tabbed editors.

    There are currently two implementations of this interface in Tasks.
    EditorAreaPane provides a simple, tabbed editor area. AdvancedEditorAreaPane
    additionally permits arbitrary splitting of the editor area so that editors
    can be displayed side-by-side.
    """

    # 'IEditorAreaPane' interface -----------------------------------------#

    #: The currently active editor.
    active_editor = Instance(IEditor)

    #: The list of all the visible editors in the pane.
    editors = List(IEditor)

    #: A list of extensions for file types to accept via drag and drop.
    #: Note: This functionality is provided because it is very common, but
    #: drag and drop support is in general highly toolkit-specific. If more
    #: sophisticated support is required, subclass an editor area
    #: implementation.
    file_drop_extensions = List(Str)

    #: A file with a supported extension was dropped into the editor area.
    file_dropped = Event(File)

    #: Whether to hide the tab bar when there is only a single editor.
    hide_tab_bar = Bool(False)

    # ------------------------------------------------------------------------
    # 'IEditorAreaPane' interface.
    # ------------------------------------------------------------------------

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """

    def add_editor(self, editor):
        """ Adds an editor to the pane.
        """

    def create_editor(self, obj, factory=None):
        """ Creates an editor for an object.

        If a factory is specified, it will be used instead of the editor factory
        registry. Otherwise, this method will return None if a suitable factory
        cannot be found in the registry.

        Note that the editor is not added to the pane.
        """

    def edit(self, obj, factory=None, use_existing=True):
        """ Edit an object.

        This is a convenience method that creates and adds an editor for the
        specified object. If 'use_existing' is set and the object is already
        being edited, then that editor will be activated and a new editor will
        not be created.

        Returns the (possibly new) editor for the object.
        """

    def get_editor(self, obj):
        """ Returns the editor for an object.

        Returns None if the object is not being edited.
        """

    def get_factory(self, obj):
        """ Returns an editor factory suitable for editing an object.

        Returns None if there is no such editor factory.
        """

    def register_factory(self, factory, filter):
        """ Registers a factory for creating editors.

        The 'factory' parameter is a callabe of form:
            callable(editor_area=editor_area, obj=obj) -> IEditor

        Often, factory will be a class that provides the 'IEditor' interface.

        The 'filter' parameter is a callable of form:
            callable(obj) -> bool

        that indicates whether the editor factory is suitable for an object.

        If multiple factories apply to a single object, it is undefined which
        factory is used. On the other hand, multiple filters may be registered
        for a single factory, in which case only one must apply for the factory
        to be selected.
        """

    def remove_editor(self, editor):
        """ Removes an editor from the pane.
        """

    def unregister_factory(self, factory):
        """ Unregisters a factory for creating editors.
        """


class MEditorAreaPane(HasTraits):

    # 'IEditorAreaPane' interface -----------------------------------------#

    active_editor = Instance(IEditor)
    editors = List(IEditor)
    file_drop_extensions = List(Str)
    file_dropped = Event(File)
    hide_tab_bar = Bool(False)

    # Protected traits -----------------------------------------------------

    _factory_map = Dict(Callable, List(Callable))

    # ------------------------------------------------------------------------
    # 'IEditorAreaPane' interface.
    # ------------------------------------------------------------------------

    def create_editor(self, obj, factory=None):
        """ Creates an editor for an object.
        """
        if factory is None:
            factory = self.get_factory(obj)

        if factory is not None:
            return factory(editor_area=self, obj=obj)

        return None

    def edit(self, obj, factory=None, use_existing=True):
        """ Edit an object.
        """
        if use_existing:
            # Is the object already being edited in the window?
            editor = self.get_editor(obj)
            if editor is not None:
                self.activate_editor(editor)
                return editor

        # If not, create an editor for it.
        editor = self.create_editor(obj, factory)
        if editor is None:
            logger.warning("Cannot create editor for obj %r", obj)

        else:
            self.add_editor(editor)
            self.activate_editor(editor)

        return editor

    def get_editor(self, obj):
        """ Returns the editor for an object.
        """
        for editor in self.editors:
            if editor.obj == obj:
                return editor
        return None

    def get_factory(self, obj):
        """ Returns an editor factory suitable for editing an object.
        """
        for factory, filters in self._factory_map.items():
            for filter_ in filters:
                # FIXME: We should swallow exceptions, but silently?
                try:
                    if filter_(obj):
                        return factory
                except:
                    pass
        return None

    def register_factory(self, factory, filter):
        """ Registers a factory for creating editors.
        """
        self._factory_map.setdefault(factory, []).append(filter)

    def unregister_factory(self, factory):
        """ Unregisters a factory for creating editors.
        """
        if factory in self._factory_map:
            del self._factory_map[factory]
