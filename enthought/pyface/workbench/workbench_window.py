""" A workbench window. """


# Standard library imports.
import cPickle
import logging
from os.path import exists, join

# Enthought library imports.
from enthought.pyface.api import ApplicationWindow
from enthought.traits.api import Callable, Constant, Event, Instance, List, Str
from enthought.traits.api import Tuple, Unicode, Vetoable, implements
from enthought.traits.api import on_trait_change

# Local imports.
from i_editor import IEditor
from i_editor_manager import IEditorManager
from i_perspective import IPerspective
from i_view import IView
from i_workbench_part import IWorkbenchPart
from perspective import Perspective
from workbench_window_layout import WorkbenchWindowLayout


# Logging.
logger = logging.getLogger(__name__)


class WorkbenchWindow(ApplicationWindow):
    """ A workbench window. """

    #### 'IWorkbenchWindow' interface #########################################

    # The view or editor that currently has the focus.
    active_part = Instance(IWorkbenchPart)
    
    # The editor manager is used to create/restore editors.
    editor_manager = Instance(IEditorManager)

    # The current selection within the window.
    selection = List

    # A directory on the local file system that we can read and write to at
    # will. This is used to persist layout information etc.
    state_location = Unicode

    # The workbench that the window belongs to.
    workbench = Instance('enthought.pyface.workbench.api.IWorkbench')
    
    #### Editors #######################

    # The active editor.
    active_editor = Instance(IEditor)

    # The visible (open) editors.
    editors = List(IEditor)

    # The Id of the editor area.
    editor_area_id = Constant('enthought.pyface.workbench.editors')

    # The (initial) size of the editor area (the user is free to resize it of
    # course).
    editor_area_size = Tuple((100, 100))

    # Fired when an editor is about to be opened (or restored).
    editor_opening = Event(IEditor)
    
    # Fired when an editor has been opened (or restored).
    editor_opened = Event(IEditor)

    # Fired when an editor is about to be closed.
    editor_closing = Event(IEditor)

    # Fired when an editor has been closed.
    editor_closed = Event(IEditor)

    #### Views #########################

    # The active view.
    active_view = Instance(IView)

    # The available views (note that this is *all* of the views, not just those
    # currently visible).
    #
    # Views *cannot* be shared between windows as each view has a reference to
    # its toolkit-specific control etc.
    views = List(IView)

    #### Perspectives ##################

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
    # If this is the empty string, then the first perspective in the list of
    # perspectives is shown (if there are no perspectives then an instance of
    # the default 'Perspective' class is used).
    #
    # If this is not the empty string then the perspective with this Id is
    # shown.
    #
    # 2. When the window is being restored.
    #
    # If this is the empty string then the last perspective that was visible
    # when the window last closed is shown.
    #
    # If this is not the empty string then the perspective with this Id is
    # shown.
    default_perspective_id = Str

    #### 'WorkbenchWindow' interface ##########################################

    # The window layout is responsible for creating and managing the internal
    # structure of the window (i.e., it knows how to add and remove views and
    # editors etc).
    layout = Instance(WorkbenchWindowLayout)

    ###########################################################################
    # 'Window' interface.
    ###########################################################################

    def open(self):
        """ Open the window.

        Overridden to make the 'opening' event vetoable.

        Return True if the window opened successfully; False if the open event
        was vetoed.

        """

        logger.debug('window %s opening', self)

        # Trait notification.
        self.opening = event = Vetoable()
        if not event.veto:
            if self.control is None:
                self._create()

            self.show(True)

            # Trait notification.
            self.opened = self

            logger.debug('window %s opened', self)

        else:
            logger.debug('window %s open was vetoed', self)

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

        logger.debug('window %s closing', self)

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

                logger.debug('window %s closed', self)

            else:
                logger.debug('window %s close was vetoed', self)

        else:
            logger.debug('window %s is not open', self)

        # FIXME v3: This is not actually part of the Pyface 'Window' API (but
        # maybe it should be). We return this to indicate whether the window
        # actually closed.  With the current implementation this will always
        # return True.
        return self.control is None
        
    ###########################################################################
    # Protected 'Window' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Create and return the window contents. """

        # Create the initial window layout.
        contents = self.layout.create_initial_layout()

        # Save the initial window layout so that we can reset it when changing
        # to a perspective that has not been seen yet.
        self._initial_layout = self.layout.get_view_memento()

        # When the application starts up we try to make it look just like it
        # did the last time it was closed down (i.e., the layout of views and
        # editors etc).
        #
        # If we have a saved layout then try to restore it (it may not be
        # totally possible, e.g. an editor may have been open for an object
        # that has been deleted outside of the application, but we try to do
        # the best we can!).
        filename = join(self.state_location, 'active_perspective_id')
        if exists(filename):
            self.restore_layout()

        # Otherwise, we have no saved layout so let's create one.
        else:
            self.active_perspective = self._get_initial_perspective()
##             self._create_layout()

        return contents

    ###########################################################################
    # 'WorkbenchWindow' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _editor_manager_default(self):
        """ Trait initializer. """

        from editor_manager import EditorManager
        
        return EditorManager(window=self)

    def _layout_default(self):
        """ Trait initializer. """

        layout = WorkbenchWindowLayout(window=self)

        # fixme: Is there a more 'traitsy' way to do this?
        def propogate(obj, trait_name):
            def handler(event):
                setattr(self, trait_name, event)
                return

            obj.on_trait_change(handler, trait_name)

            return
        
        propogate(layout, 'editor_opening')
        propogate(layout, 'editor_opened')
        propogate(layout, 'editor_closing')
        propogate(layout, 'editor_closed')

        return layout

    def _state_location_default(self):
        """ Trait initializer. """

        return self.workbench.state_location
    
    #### Methods ##############################################################

    def activate_editor(self, editor):
        """ Activates an editor. """

        self.layout.activate_editor(editor)

        return

    def activate_view(self, view):
        """ Activates a view. """

        self.layout.activate_view(view)
        
        return

    def add_editor(self, editor, title=None):
        """ Adds an editor.

        If no title is specified, the editor's name is used.

        """

        if title is None:
            title = editor.name

        self.layout.add_editor(editor, title)
        self.editors.append(editor)

        return

    def add_view(self, view, position, relative_to=None, size=(-1, -1)):
        """ Adds a view. """

        self.layout.add_view(view, position, relative_to, size)

        return

    def close_editor(self, editor):
        """ Closes an editor. """

        self.layout.close_editor(editor)

        return

    def close_view(self, view):
        """ Closes a view.

        fixme: Currently views are never 'closed' in the same sense as an
        editor is closed. Views are merely hidden.

        """

        self.hide_view(view)

        return

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

        return
    
    def destroy_views(self, views):
        """ Destroy a list of views. """

        for view in views:
            if view.control is not None:
                view.destroy_control()

        return
    
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
            logger.warn('no editor for object %s', obj)

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
        
        return

    def hide_view(self, view):
        """ Hide a view. """

        self.layout.hide_view(view)

        return

    def refresh(self):
        """ Refresh the window to reflect any changes. """

        self.layout.refresh()

        return

    def reset_editors(self):
        """ Activate the first editor in every tab. """

        self.layout.reset_editors()

        return

    def reset_views(self):
        """ Activate the first view in every tab. """

        self.layout.reset_views()

        return

    def show_editor_area(self):
        """ Show the editor area. """
        
        self.layout.show_editor_area()
        
        return

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

    #### Methods for saving and restoring the layout ##########################

    # fixme: This is called from workbench on exit to persist the window
    # layout.
    #
    # fixme: Can we replace these with memento methods and let the workbench
    # decide how to persist the memento?!?
##     def get_memento(self):
##         """ Return the state of the window suitable for pickling etc. """

##         memento = (
##             self.active_perspective.id,
##             self.layout.get_view_memento(),
##             self.layout.get_editor_memento()
##         )

##         return memento

##     def set_memento(self, memento):
##         """ Restore the state of the window from a memento. """

##         active_perspective_id, view_memento, editor_memento = memento

##         return
            
    def save_layout(self):
        """ Saves the window layout. """

        # Save the Id of the active perspective.
        f = file(join(self.state_location, 'active_perspective_id'), 'w')
        f.write(self.active_perspective.id)
        f.close()

        # Save the layout of the view area.
        memento = self.layout.get_view_memento()

        f = file(join(self.state_location, self.active_perspective.id), 'w')
        cPickle.dump(memento, f)
        f.close()

        # Save the layout of the editor area.
        memento = self.layout.get_editor_memento()

        f = file(join(self.state_location, 'editors'), 'w')
        cPickle.dump(memento, f)
        f.close()

        return

    # fixme: This is only ever called internally!
    def restore_layout(self):
        """ Restores the window layout. """

        # The layout of the view area is restored in the 'active_perspective'
        # trait change handler!
        self.active_perspective = self._get_initial_perspective()

        # Restore the layout of the editor area.
        filename = join(self.state_location, 'editors')
        if exists(filename):
            f = file(filename)
            memento = cPickle.load(f)
            f.close()

            self.layout.set_editor_memento(memento)

        return

    ###########################################################################
    # Private interface.
    ###########################################################################

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

        return

##     def _create_layout(self):
##         """ Creates the initial window layout. """

##         perspective = self._get_initial_perspective()

##         if len(self.perspectives) > 0:
##             if len(self.default_perspective_id) > 0:
##                 perspective = self.get_perspective_by_id(
##                     self.default_perspective_id
##                 )

##             else:
##                 perspective = self.perspectives[0]

##         else:
##             perspective = Perspective()

##         # All the work is done in the 'active_perspective' trait change
##         # handler!
##         self.active_perspective = perspective

##         return

##     def _add_view_listeners(self, view):
##         """ Adds any required listeners to a view. """

##         view.window = self

##         # Update our selection when the selection of any contained view
##         # changes.
##         #
##         # fixme: Not sure this is really what we want to do but it is what
##         # we did in the old UI plugin and the selection listener still does
##         # only listen to the window's selection.
##         view.on_trait_change(self._on_view_selection_changed, 'selection')

##         return
    
##     def _remove_view_listeners(self, view):
##         """ Removes any required listeners from a view. """

##         view.window = None

##         # Remove the selection listener.
##         view.on_trait_change(
##             self._on_view_selection_changed, 'selection', remove=True
##         )
        
##         return

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
            self._get_first_perspective
        ]

        for method in methods:
            perspective = method()
            if perspective is not None:
                break

        # If we have no known perspectives, make a new blank one up.
        else:
            logger.warn('no known perspectives - creating a new one')
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
                logger.warn('default perspective %s no longer available', id)

        else:
            perspective = None
            
        return perspective

    def _get_previous_perspective(self):
        """ Return the previous perspective.

        Return None if there has been no previous perspective or it no longer
        exists.

        """

        try:
            f = file(join(self.state_location, 'active_perspective_id'), 'r')
            id = f.read()
            f.close()

            perspective = self.get_perspective_by_id(id)
            if perspective is None:
                logger.warn('previous perspective %s no longer available', id)

        except:
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
        active_view_id = self.active_view and self.active_view.id or None
        
        memento = (
            self.layout.get_view_memento(), active_view_id
        )

        f = file(join(self.state_location, perspective.id), 'w')
        cPickle.dump(memento, f)
        f.close()

        return

    def _show_perspective(self, old, new):
        """ Show a perspective. """

        # Save the Id of the active perspective.
        f = file(join(self.state_location, 'active_perspective_id'), 'w')
        f.write(new.id)
        f.close()

        # If the perspective has been seen before then restore it.
        filename = join(self.state_location, new.id)
        if exists(filename):
            # Load the window layout from the specified file.
            f = file(filename)
            memento = cPickle.load(f)
            f.close()

            # fixme: Backwards compatability!
            if type(memento) is tuple:
                view_memento, active_view_id = memento

            else:
                view_memento = memento
                active_view_id = None
                
            self.layout.set_view_memento(view_memento)

            # Make sure the active part, view and editor reflect the new
            # perspective.
            view = self.get_view_by_id(active_view_id)
            if view is not None:
                self.active_view = view
                
            if not self.show_editor_area:
                self.active_editor = None
        
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

            if not self.show_editor_area:
                self.active_editor = None

            # Show the editor area?
            if new.show_editor_area:
                self.show_editor_area()

            else:
                self.hide_editor_area()
                self.active_editor = None
            
        # This forces the dock window to update its layout.
        if old is not None:
            self.refresh()

        perspective = new
        print 'Show perspective', perspective.id
        print 'Active part', self.active_part
        print 'Active view', self.active_view
        print 'Active editor', self.active_editor

        return
    
    #### Trait change handlers ################################################

    #### Static ####

    def _active_perspective_changed(self, old, new):
        """ Static trait change handler. """

        logger.debug('active perspective changed from %s to %s', old, new)

        # Hide the old perspective...
        if old is not None:
            self._hide_perspective(old)
                
        # ... and show the new one.
        if new is not None:
            self._show_perspective(old, new)

        return

    def _active_editor_changed(self, old, new):
        """ Static trait change handler. """

        logger.debug('active editor changed from %s to %s', old, new)
        self.active_part = new
        
        return

    def _active_part_changed(self, old, new):
        """ Static trait change handler. """

        if new is None:
            self.selection = []

        else:
            self.selection = new.selection

        logger.debug('active part changed from %s to %s', old, new)

        return

    def _active_view_changed(self, old, new):
        """ Static trait change handler. """

        logger.debug('active view changed from %s to %s', old, new)
        self.active_part = new

        return

    def _views_changed(self, old, new):
        """ Static trait change handler. """

        # Cleanup any old views.
        for view in old:
            view.window = None
            
        # Initialize any new views.
        for view in new:
            view.window = self

        return

    def _views_items_changed(self, event):
        """ Static trait change handler. """

        # Cleanup any old views.
        for view in event.removed:
            view.window = None

        # Initialize any new views.
        for view in event.added:
            view.window = self

        return

    #### Dynamic ####

    @on_trait_change('editors.has_focus')
    def _has_focus_changed_for_editor(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """

        if trait_name == 'has_focus' and new:
            self.active_editor = obj

        return

    @on_trait_change('views.has_focus')
    def _has_focus_changed_for_view(self, obj, trait_name, old, new):
        """ Dynamic trait change handler. """
        
        if trait_name == 'has_focus' and new:
            self.active_view = obj

        return
    
#### EOF ######################################################################
