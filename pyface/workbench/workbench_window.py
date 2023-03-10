# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A workbench window. """


import logging


from pyface.api import ApplicationWindow, GUI
from traits.api import (
    Constant,
    Delegate,
    Instance,
    List,
    Str,
    Tuple,
    Undefined,
    Vetoable,
    observe,
)

from .i_editor import IEditor
from .i_editor_manager import IEditorManager
from .i_perspective import IPerspective
from .i_view import IView
from .i_workbench_part import IWorkbenchPart
from .perspective import Perspective
from .workbench_window_layout import WorkbenchWindowLayout
from .workbench_window_memento import WorkbenchWindowMemento


# Logging.
logger = logging.getLogger(__name__)


class WorkbenchWindow(ApplicationWindow):
    """ A workbench window. """

    # 'IWorkbenchWindow' interface -----------------------------------------

    # The view or editor that currently has the focus.
    active_part = Instance(IWorkbenchPart)

    # The editor manager is used to create/restore editors.
    editor_manager = Instance(IEditorManager)

    # The current selection within the window.
    selection = List()

    # The workbench that the window belongs to.
    workbench = Instance("pyface.workbench.api.IWorkbench")

    # Editors -----------------------

    # The active editor.
    active_editor = Instance(IEditor)

    # The visible (open) editors.
    editors = List(IEditor)

    # The Id of the editor area.
    editor_area_id = Constant("pyface.workbench.editors")

    # The (initial) size of the editor area (the user is free to resize it of
    # course).
    editor_area_size = Tuple((100, 100))

    # Fired when an editor is about to be opened (or restored).
    editor_opening = Delegate("layout")  # Event(IEditor)

    # Fired when an editor has been opened (or restored).
    editor_opened = Delegate("layout")  # Event(IEditor)

    # Fired when an editor is about to be closed.
    editor_closing = Delegate("layout")  # Event(IEditor)

    # Fired when an editor has been closed.
    editor_closed = Delegate("layout")  # Event(IEditor)

    # Views -------------------------

    # The active view.
    active_view = Instance(IView)

    # The available views (note that this is *all* of the views, not just those
    # currently visible).
    #
    # Views *cannot* be shared between windows as each view has a reference to
    # its toolkit-specific control etc.
    views = List(IView)

    # Perspectives -----------------#

    # The active perspective.
    active_perspective = Instance(IPerspective)

    # The available perspectives. If no perspectives are specified then the
    # a single instance of the 'Perspective' class is created.
    perspectives = List(IPerspective)

    # The Id of the default perspective.
    #
    # There are two situations in which this is used:
    #
    # 1. When the window is being created from scratch (i.e., not restored).
    #
    #    If this is the empty string, then the first perspective in the list of
    #    perspectives is shown (if there are no perspectives then an instance
    #    of the default 'Perspective' class is used). If this is *not* the
    #    empty string then the perspective with this Id is shown.
    #
    # 2. When the window is being restored.
    #
    #    If this is the empty string, then the last perspective that was
    #    visible when the window last closed is shown. If this is not the empty
    #    string then the perspective with this Id is shown.
    #
    default_perspective_id = Str()

    # 'WorkbenchWindow' interface -----------------------------------------#

    # The window layout is responsible for creating and managing the internal
    # structure of the window (i.e., it knows how to add and remove views and
    # editors etc).
    layout = Instance(WorkbenchWindowLayout)

    # 'Private' interface -------------------------------------------------#

    # The state of the window suitable for pickling etc.
    _memento = Instance(WorkbenchWindowMemento)

    # ------------------------------------------------------------------------
    # 'Window' interface.
    # ------------------------------------------------------------------------

    def open(self):
        """ Open the window.

        Overridden to make the 'opening' event vetoable.

        Return True if the window opened successfully; False if the open event
        was vetoed.

        """

        logger.debug("window %s opening", self)

        # Trait notification.
        self.opening = event = Vetoable()
        if not event.veto:
            if self.control is None:
                self.create()

            self.show(True)

            # Trait notification.
            self.opened = self

            logger.debug("window %s opened", self)

        else:
            logger.debug("window %s open was vetoed", self)

        # fixme: This is not actually part of the Pyface 'Window' API (but
        # maybe it should be). We return this to indicate whether the window
        # actually opened.
        return self.control is not None

    def close(self):
        """ Closes the window.

        Overridden to make the 'closing' event vetoable.

        Return True if the window closed successfully (or was not even open!),
        False if the close event was vetoed.

        """

        logger.debug("window %s closing", self)

        if self.control is not None:
            # Trait notification.
            self.closing = event = Vetoable()

            # fixme: Hack to mimic vetoable events!
            if not event.veto:
                # Give views and editors a chance to cleanup after themselves.
                self.destroy_views(self.views)
                self.destroy_editors(self.editors)

                # Cleanup the window layout (event handlers, etc.)
                self.layout.close()

                # Cleanup the toolkit-specific control.
                self.destroy()

                # Cleanup our reference to the control so that we can (at least
                # in theory!) be opened again.
                self.control = None

                # Trait notification.
                self.closed = self

                logger.debug("window %s closed", self)

            else:
                logger.debug("window %s close was vetoed", self)

        else:
            logger.debug("window %s is not open", self)

        # FIXME v3: This is not actually part of the Pyface 'Window' API (but
        # maybe it should be). We return this to indicate whether the window
        # actually closed.
        return self.control is None

    # ------------------------------------------------------------------------
    # Protected 'Window' interface.
    # ------------------------------------------------------------------------

    def _create_contents(self, parent):
        """ Create and return the window contents. """

        # Create the initial window layout.
        contents = self.layout.create_initial_layout(parent)

        # Save the initial window layout so that we can reset it when changing
        # to a perspective that has not been seen yet.
        self._initial_layout = self.layout.get_view_memento()

        # Are we creating the window from scratch or restoring it from a
        # memento?
        if self._memento is None:
            self._memento = WorkbenchWindowMemento()

        else:
            self._restore_contents()

        # Set the initial perspective.
        self.active_perspective = self._get_initial_perspective()

        return contents

    # ------------------------------------------------------------------------
    # 'WorkbenchWindow' interface.
    # ------------------------------------------------------------------------

    # Initializers ---------------------------------------------------------

    def _editor_manager_default(self):
        """ Trait initializer. """

        from .editor_manager import EditorManager

        return EditorManager(window=self)

    def _layout_default(self):
        """ Trait initializer. """

        return WorkbenchWindowLayout(window=self)

    # Methods -------------------------------------------------------------#

    def activate_editor(self, editor):
        """ Activates an editor. """

        self.layout.activate_editor(editor)

    def activate_view(self, view):
        """ Activates a view. """

        self.layout.activate_view(view)

    def add_editor(self, editor, title=None):
        """ Adds an editor.

        If no title is specified, the editor's name is used.

        """

        if title is None:
            title = editor.name

        self.layout.add_editor(editor, title)
        self.editors.append(editor)

    def add_view(self, view, position=None, relative_to=None, size=(-1, -1)):
        """ Adds a view. """

        self.layout.add_view(view, position, relative_to, size)

        # This case allows for views that are created and added dynamically
        # (i.e. they were not even known about when the window was created).
        if view not in self.views:
            self.views.append(view)

    def close_editor(self, editor):
        """ Closes an editor. """

        self.layout.close_editor(editor)

    def close_view(self, view):
        """ Closes a view.

        fixme: Currently views are never 'closed' in the same sense as an
        editor is closed. Views are merely hidden.

        """

        self.hide_view(view)

    def create_editor(self, obj, kind=None):
        """ Create an editor for an object.

        Return None if no editor can be created for the object.

        """

        return self.editor_manager.create_editor(self, obj, kind)

    def destroy_editors(self, editors):
        """ Destroy a list of editors. """

        for editor in editors:
            if editor.control is not None:
                editor.destroy_control()

    def destroy_views(self, views):
        """ Destroy a list of views. """

        for view in views:
            if view.control is not None:
                view.destroy_control()

    def edit(self, obj, kind=None, use_existing=True):
        """ Edit an object.

        'kind' is simply passed through to the window's editor manager to
        allow it to create a particular kind of editor depending on context
        etc.

        If 'use_existing' is True and the object is already being edited in
        the window then the existing editor will be activated (i.e., given
        focus, brought to the front, etc.).

        If 'use_existing' is False, then a new editor will be created even if
        one already exists.

        """

        if use_existing:
            # Is the object already being edited in the window?
            editor = self.get_editor(obj, kind)

            if editor is not None:
                # If so, activate the existing editor (i.e., bring it to the
                # front, give it the focus etc).
                self.activate_editor(editor)
                return editor

        # Otherwise, create an editor for it.
        editor = self.create_editor(obj, kind)

        if editor is None:
            logger.warning("no editor for object %s", obj)

        self.add_editor(editor)
        self.activate_editor(editor)

        return editor

    def get_editor(self, obj, kind=None):
        """ Return the editor that is editing an object.

        Return None if no such editor exists.

        """

        return self.editor_manager.get_editor(self, obj, kind)

    def get_editor_by_id(self, id):
        """ Return the editor with the specified Id.

        Return None if no such editor exists.

        """

        for editor in self.editors:
            if editor.id == id:
                break

        else:
            editor = None

        return editor

    def get_part_by_id(self, id):
        """ Return the workbench part with the specified Id.

        Return None if no such part exists.

        """

        return self.get_view_by_id(id) or self.get_editor_by_id(id)

    def get_perspective_by_id(self, id):
        """ Return the perspective with the specified Id.

        Return None if no such perspective exists.

        """

        for perspective in self.perspectives:
            if perspective.id == id:
                break

        else:
            if id == Perspective.DEFAULT_ID:
                perspective = Perspective()

            else:
                perspective = None

        return perspective

    def get_perspective_by_name(self, name):
        """ Return the perspective with the specified name.

        Return None if no such perspective exists.

        """

        for perspective in self.perspectives:
            if perspective.name == name:
                break

        else:
            perspective = None

        return perspective

    def get_view_by_id(self, id):
        """ Return the view with the specified Id.

        Return None if no such view exists.

        """

        for view in self.views:
            if view.id == id:
                break

        else:
            view = None

        return view

    def hide_editor_area(self):
        """ Hide the editor area. """

        self.layout.hide_editor_area()

    def hide_view(self, view):
        """ Hide a view. """

        self.layout.hide_view(view)

    def refresh(self):
        """ Refresh the window to reflect any changes. """

        self.layout.refresh()

    def reset_active_perspective(self):
        """ Reset the active perspective back to its original contents. """

        perspective = self.active_perspective

        # If the perspective has been seen before then delete its memento.
        if perspective.id in self._memento.perspective_mementos:
            # Remove the perspective's memento.
            del self._memento.perspective_mementos[perspective.id]

        # Re-display the perspective (because a memento no longer exists for
        # the perspective, its 'create_contents' method will be called again).
        self._show_perspective(perspective, perspective)

    def reset_all_perspectives(self):
        """ Reset all perspectives back to their original contents. """

        # Remove all perspective mementos (except user perspectives).
        for id in self._memento.perspective_mementos.keys():
            if not id.startswith("__user_perspective"):
                del self._memento.perspective_mementos[id]

        # Re-display the active perspective.
        self._show_perspective(
            self.active_perspective, self.active_perspective
        )

    def reset_editors(self):
        """ Activate the first editor in every tab. """

        self.layout.reset_editors()

    def reset_views(self):
        """ Activate the first view in every tab. """

        self.layout.reset_views()

    def show_editor_area(self):
        """ Show the editor area. """

        self.layout.show_editor_area()

    def show_view(self, view):
        """ Show a view. """

        # If the view is already in the window layout, but hidden, then just
        # show it.
        #
        # fixme: This is a little gorpy, reaching into the window layout here,
        # but currently this is the only thing that knows whether or not the
        # view exists but is hidden.
        if self.layout.contains_view(view):
            self.layout.show_view(view)

        # Otherwise, we have to add the view to the layout.
        else:
            self._add_view_in_default_position(view)
            self.refresh()

        return

    # Methods for saving and restoring the layout -------------------------#

    def get_memento(self):
        """ Return the state of the window suitable for pickling etc. """

        # The size and position of the window.
        self._memento.size = self.size
        self._memento.position = self.position

        # The Id of the active perspective.
        self._memento.active_perspective_id = self.active_perspective.id

        # The layout of the active perspective.
        self._memento.perspective_mementos[self.active_perspective.id] = (
            self.layout.get_view_memento(),
            self.active_view and self.active_view.id or None,
            self.layout.is_editor_area_visible(),
        )

        # The layout of the editor area.
        self._memento.editor_area_memento = self.layout.get_editor_memento()

        # Any extra toolkit-specific data.
        self._memento.toolkit_data = self.layout.get_toolkit_memento()

        return self._memento

    def set_memento(self, memento):
        """ Restore the state of the window from a memento. """

        # All we do here is save a reference to the memento - we don't actually
        # do anything with it until the window is opened.
        #
        # This obviously means that you can't set the memento of a window
        # that is already open, but I can't see a use case for that anyway!
        self._memento = memento

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _add_view_in_default_position(self, view):
        """ Adds a view in its 'default' position. """

        # Is the view in the current perspectives contents list? If it is then
        # we use the positioning information in the perspective item. Otherwise
        # we will use the default positioning specified in the view itself.
        item = self._get_perspective_item(self.active_perspective, view)
        if item is None:
            item = view

        # fixme: This only works because 'PerspectiveItem' and 'View' have the
        # identical 'position', 'relative_to', 'width' and 'height' traits! We
        # need to unify these somehow!
        relative_to = self.get_view_by_id(item.relative_to)
        size = (item.width, item.height)

        self.add_view(view, item.position, relative_to, size)

    def _get_initial_perspective(self, *methods):
        """ Return the initial perspective. """

        methods = [
            # If a default perspective was specified then we prefer that over
            # any other perspective.
            self._get_default_perspective,
            # If there was no default perspective then try the perspective that
            # was active the last time the application was run.
            self._get_previous_perspective,
            # If there was no previous perspective, then try the first one that
            # we know about.
            self._get_first_perspective,
        ]

        for method in methods:
            perspective = method()
            if perspective is not None:
                break

        # If we have no known perspectives, make a new blank one up.
        else:
            logger.warning("no known perspectives - creating a new one")
            perspective = Perspective()

        return perspective

    def _get_default_perspective(self):
        """ Return the default perspective.

        Return None if no default perspective was specified or it no longer
        exists.

        """

        id = self.default_perspective_id

        if len(id) > 0:
            perspective = self.get_perspective_by_id(id)
            if perspective is None:
                logger.warning("default perspective %s no longer available", id)

        else:
            perspective = None

        return perspective

    def _get_previous_perspective(self):
        """ Return the previous perspective.

        Return None if there has been no previous perspective or it no longer
        exists.

        """

        id = self._memento.active_perspective_id

        if len(id) > 0:
            perspective = self.get_perspective_by_id(id)
            if perspective is None:
                logger.warning("previous perspective %s no longer available", id)

        else:
            perspective = None

        return perspective

    def _get_first_perspective(self):
        """ Return the first perspective in our list of perspectives.

        Return None if no perspectives have been defined.

        """

        if len(self.perspectives) > 0:
            perspective = self.perspectives[0]

        else:
            perspective = None

        return perspective

    def _get_perspective_item(self, perspective, view):
        """ Return the perspective item for a view.

        Return None if the view is not mentioned in the perspectives contents.

        """

        # fixme: Errrr, shouldn't this be a method on the window?!?
        for item in perspective.contents:
            if item.id == view.id:
                break

        else:
            item = None

        return item

    def _hide_perspective(self, perspective):
        """ Hide a perspective. """

        # fixme: This is a bit ugly but... when we restore the layout we ignore
        # the default view visibility.
        for view in self.views:
            view.visible = False

        # Save the current layout of the perspective.
        self._memento.perspective_mementos[perspective.id] = (
            self.layout.get_view_memento(),
            self.active_view and self.active_view.id or None,
            self.layout.is_editor_area_visible(),
        )

    def _show_perspective(self, old, new):
        """ Show a perspective. """

        # If the perspective has been seen before then restore it.
        memento = self._memento.perspective_mementos.get(new.id)

        if memento is not None:
            # Show the editor area?
            # We need to set the editor area before setting the views
            if len(memento) == 2:
                logger.warning("Restoring perspective from an older version.")
                editor_area_visible = True
            else:
                editor_area_visible = memento[2]

            # Show the editor area if it is set to be visible
            if editor_area_visible:
                self.show_editor_area()
            else:
                self.hide_editor_area()
                self.active_editor = None

            # Now set the views
            view_memento, active_view_id = memento[:2]
            self.layout.set_view_memento(view_memento)

            # Make sure the active part, view and editor reflect the new
            # perspective.
            view = self.get_view_by_id(active_view_id)
            if view is not None:
                self.active_view = view

        # Otherwise, this is the first time the perspective has been seen
        # so create it.
        else:
            if old is not None:
                # Reset the window layout to its initial state.
                self.layout.set_view_memento(self._initial_layout)

            # Create the perspective in the window.
            new.create(self)

            # Make sure the active part, view and editor reflect the new
            # perspective.
            self.active_view = None

            # Show the editor area?
            if new.show_editor_area:
                self.show_editor_area()
            else:
                self.hide_editor_area()
                self.active_editor = None

        # Inform the perspective that it has been shown.
        new.show(self)

        # This forces the dock window to update its layout.
        if old is not None:
            self.refresh()

    def _restore_contents(self):
        """ Restore the contents of the window. """

        self.layout.set_editor_memento(self._memento.editor_area_memento)

        self.size = self._memento.size
        self.position = self._memento.position

        # Set the toolkit-specific data last because it may override the generic
        # implementation.
        # FIXME: The primary use case is to let Qt restore the window's geometry
        # wholesale, including maximization state. If we ever go Qt-only, this
        # is a good area to refactor.
        self.layout.set_toolkit_memento(self._memento)

        return

    # Trait change handlers ------------------------------------------------

    # Static ----

    def _active_perspective_changed(self, old, new):
        """ Static trait change handler. """

        logger.debug("active perspective changed from <%s> to <%s>", old, new)

        # Hide the old perspective...
        if old is not None:
            self._hide_perspective(old)

        # ... and show the new one.
        if new is not None:
            self._show_perspective(old, new)

    def _active_editor_changed(self, old, new):
        """ Static trait change handler. """

        logger.debug("active editor changed from <%s> to <%s>", old, new)
        self.active_part = new

    def _active_part_changed(self, old, new):
        """ Static trait change handler. """

        if new is None:
            self.selection = []

        else:
            self.selection = new.selection

        logger.debug("active part changed from <%s> to <%s>", old, new)

    def _active_view_changed(self, old, new):
        """ Static trait change handler. """

        logger.debug("active view changed from <%s> to <%s>", old, new)
        self.active_part = new

    def _views_changed(self, old, new):
        """ Static trait change handler. """

        # Cleanup any old views.
        for view in old:
            view.window = None

        # Initialize any new views.
        for view in new:
            view.window = self

    def _views_items_changed(self, event):
        """ Static trait change handler. """

        # Cleanup any old views.
        for view in event.removed:
            view.window = None

        # Initialize any new views.
        for view in event.added:
            view.window = self

        return

    # Dynamic ----

    @observe("layout:editor_closed")
    def _on_editor_closed(self, event):
        """ Dynamic trait change handler. """

        if event.new is None or event.new is Undefined:
            return
        index = self.editors.index(event.new)
        del self.editors[index]
        if event.new is self.active_editor:
            if len(self.editors) > 0:
                index = min(index, len(self.editors) - 1)
                # If the user closed the editor manually then this method is
                # being called from a toolkit-specific event handler. Because
                # of that we have to make sure that we don't change the focus
                # from within this method directly hence we activate the editor
                # later in the GUI thread.
                GUI.invoke_later(self.activate_editor, self.editors[index])

            else:
                self.active_editor = None

        return

    @observe("editors:items:has_focus")
    def _on_editor_has_focus_changed(self, event):
        """ Dynamic trait change handler. """

        if event.new:
            self.active_editor = event.object

        return

    @observe("views:items:has_focus")
    def _has_focus_changed_for_view(self, event):
        """ Dynamic trait change handler. """

        if event.new:
            self.active_view = event.object

        return

    @observe("views:items:visible")
    def _visible_changed_for_view(self, event):
        """ Dynamic trait change handler. """

        if not event.new:
            if event.object is self.active_view:
                self.active_view = None

        return
