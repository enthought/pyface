#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------

# Standard library imports.
import cPickle

# Major library imports.
import wx

# Enthought library imports.
from enthought.logger.api import logger
from enthought.pyface.dock.api import DOCK_BOTTOM, DOCK_LEFT, DOCK_RIGHT
from enthought.pyface.dock.api import DOCK_TOP
from enthought.pyface.dock.api import DockControl, DockRegion, DockSection
from enthought.pyface.dock.api import DockSizer
from enthought.traits.ui.dockable_view_element import DockableViewElement

# Local imports.
from editor_set_structure_handler import EditorSetStructureHandler
from view_set_structure_handler import ViewSetStructureHandler
from workbench_dock_window import WorkbenchDockWindow


# Mapping from view position to the appropriate dock window constant.
POSITION_MAP = {
    'top'    : DOCK_TOP,
    'bottom' : DOCK_BOTTOM,
    'left'   : DOCK_LEFT,
    'right'  : DOCK_RIGHT
}


class WorkbenchWindowLayout_wx(object):
    """ The WorkbenchWindowLayout monkey patch for wx. """

    ###########################################################################
    # Private interface.
    ###########################################################################

    # fixme: Make the view dock window a sub class of dock window, and add
    # 'add_with' and 'add_relative_to' as methods on that.
    #
    # fixme: This is a good idea in theory, but the sizing is a bit iffy, as
    # it requires the window to be passed in to calculate the relative size
    # of the control. We could just calculate that here and pass in absolute
    # pixel sizes to the dock window subclass?
    def _add_view_relative(self, dock_control, relative_to, position, size):
        """ Adds a view relative to another item. """

        # If no 'relative to' Id is specified then we assume that the position
        # is relative to the editor area.
        if relative_to is None:
            relative_to_item = self._view_dock_window.get_control(
                self.editor_area_id, visible_only=False
            )

        # Find the item that we are adding the view relative to.
        else:
            relative_to_item = self._view_dock_window.get_control(
                relative_to.id
            )

        # Set the size of the dock control.
        self._set_item_size(dock_control, size)

        # The parent of a dock control is a dock region.
        region  = relative_to_item.parent
        section = region.parent
        section.add(dock_control, region, POSITION_MAP[position])

        return

    def _add_view_with(self, dock_control, with_obj):
        """ Adds a view in the same region as another item. """

        # Find the item that we are adding the view 'with'.
        with_item = self._view_dock_window.get_control(with_obj.id)
        if with_item is None:
            raise ValueError('Cannot find item %s' % with_obj)

        # The parent of a dock control is a dock region.
        with_item.parent.add(dock_control)

        return

    def _create_editor_dock_control(self, editor):
        """ Creates a dock control that contains the specified editor. """

        # Get the editor's toolkit-specific control.
        control = self._get_editor_control(editor)

        # Wrap a dock control around it.
        editor_dock_control = DockControl(
            id        = editor.id,
            name      = editor.name,
            closeable = True,
            control   = editor.control,
            style     = 'tab'
        )

        # Hook up the 'on_close' and trait change handlers etc.
        self._initialize_editor_dock_control(editor, editor_dock_control)

        return editor_dock_control

    def _create_view_dock_control(self, view):
        """ Creates a dock control that contains the specified view. """

        # Get the view's toolkit-specific control.
        control = self._get_view_control(view)

        # Wrap a dock control around it.
        view_dock_control = DockControl(
            id        = view.id,
            name      = view.name,
            # fixme: We would like to make views closeable, but closing via the
            # tab is different than calling show(False, layout=True) on the
            # control! If we use a close handler can we change that?!?
            closeable = False,
            control   = control,
            style     = 'tab'
        )

        # Hook up the 'on_close' and trait change handlers etc.
        self._initialize_view_dock_control(view, view_dock_control)

        return view_dock_control

    def _get_editor_control(self, editor):
        """ Returns the editor's toolkit-specific control.

        If the editor has not yet created its control, we will ask it to create
        it here.

        """

        if editor.control is None:
            parent = self._editor_dock_window.control

            # This is the toolkit-specific control that represents the 'guts'
            # of the editor.
            self.editor_opening = editor
            editor.control = editor.create_control(parent)
            self.editor_opened = editor

            # Hook up toolkit-specific events that are managed by the framework
            # etc.
            self._initialize_editor_control(editor)

        return editor.control

    def _initialize_editor_control(self, editor):
        """ Initializes the toolkit-specific control for an editor.

        This is used to hook events managed by the framework etc.

        """

        def on_set_focus(event):
            """ Called when the control gets the focus. """

            editor.has_focus = True

            # Let the default wx event handling do its thang.
            event.Skip()

            return

        def on_kill_focus(event):
            """ Called when the control loses the focus. """

            editor.has_focus = False

            # Let the default wx event handling do its thang.
            event.Skip()

            return

        self._add_focus_listeners(editor.control, on_set_focus, on_kill_focus)

        return

    def _get_editor_references(self):
        """ Returns a reference to every editor. """

        editor_manager = self.window.editor_manager
        
        editor_references = {}
        for editor in self.window.editors:
            # Create the editor reference.
            #
            # If the editor manager returns 'None' instead of a resource
            # reference then this editor will not appear the next time the
            # workbench starts up. This is useful for things like text files
            # that have an editor but have NEVER been saved.
            editor_reference = editor_manager.get_editor_memento(editor)
            if editor_reference is not None:
                editor_references[editor.id] = editor_reference

            else:
                logger.debug('not saving reference for [%s]', editor.id)

        return editor_references

    def _get_view_control(self, view):
        """ Returns a view's toolkit-specific control.

        If the view has not yet created its control, we will ask it to create
        it here.

        """

        if view.control is None:
            parent = self._view_dock_window.control

            # Make sure that the view knows which window it is in.
            view.window = self.window
            
            # This is the toolkit-specific control that represents the 'guts'
            # of the view.
            view.control = view.create_control(parent)

            # Hook up toolkit-specific events that are managed by the
            # framework etc.
            self._initialize_view_control(view)

        return view.control

    def _initialize_view_control(self, view):
        """ Initializes the toolkit-specific control for a view.

        This is used to hook events managed by the framework.

        """

        def on_set_focus(event):
            """ Called when the control gets the focus. """

            view.has_focus = True

            # Make sure that the window selection reflects the change of view.
            self.window.selection = view.selection

            # Let the default wx event handling do its thang.
            event.Skip()

            return

        def on_kill_focus(event):
            """ Called when the control loses the focus. """

            view.has_focus = False

            # Let the default wx event handling do its thang.
            event.Skip()

            return

        self._add_focus_listeners(view.control, on_set_focus, on_kill_focus)

        return

    def _add_focus_listeners(self, control, on_set_focus, on_kill_focus):
        """ Recursively adds focus listeners to a control. """

        # NOTE: If we are passed a wx control that isn't correctly initialized
        # (like when the TraitsUIView isn't properly creating it) but it is
        # actually a wx control, then we get weird exceptions from trying to
        # register event handlers.  The exception messages complain that
        # the passed control is a str object instead of a wx object.
        wx.EVT_SET_FOCUS(control, on_set_focus)
        wx.EVT_KILL_FOCUS(control, on_kill_focus)

        for child in control.GetChildren():
            self._add_focus_listeners(child, on_set_focus, on_kill_focus)

        return

    def _initialize_editor_dock_control(self, editor, editor_dock_control):
        """ Initializes an editor dock control.

        fixme: We only need this method because of a problem with the dock
        window API in the 'SetStructureHandler' class. Currently we do not get
        a reference to the dock control in 'resolve_id' and hence we cannot set
        up the 'on_close' and trait change handlers etc.

        """

        # Some editors append information to their name to indicate status (in
        # our case this is often a 'dirty' indicator that shows when the
        # contents of an editor have been modified but not saved). When the
        # dock window structure is persisted it contains the name of each dock
        # control, which obviously includes any appended state information.
        # Here we make sure that when the dock control is recreated its name is
        # set to the editor name and nothing more!
        editor_dock_control.set_name(editor.name)

        # fixme: Should we roll the traits UI stuff into the default editor.
        if hasattr(editor, 'ui') and editor.ui is not None:
            # This makes the control draggable outside of the main window.
            #editor_dock_control.export = 'enthought.pyface.workbench.editor'
            editor_dock_control.dockable = DockableViewElement(
                should_close=True, ui=editor.ui
            )

        editor_dock_control.on_close = self._on_editor_closed

        def on_id_changed():
            editor_dock_control.id = editor.id
            return

        editor.on_trait_change(on_id_changed, 'id')

        def on_name_changed():
            editor_dock_control.set_name(editor.name)
            return

        editor.on_trait_change(on_name_changed, 'name')

        return

    def _initialize_view_dock_control(self, view, view_dock_control):
        """ Initializes a view dock control.

        fixme: We only need this method because of a problem with the dock
        window API in the 'SetStructureHandler' class. Currently we do not get
        a reference to the dock control in 'resolve_id' and hence we cannot set
        up the 'on_close' and trait change handlers etc.

        """

        # Some views append information to their name to indicate status (in
        # our case this is often a 'dirty' indicator that shows when the
        # contents of a view have been modified but not saved). When the
        # dock window structure is persisted it contains the name of each dock
        # control, which obviously includes any appended state information.
        # Here we make sure that when the dock control is recreated its name is
        # set to the view name and nothing more!
        view_dock_control.set_name(view.name)

        # fixme: Should we roll the traits UI stuff into the default editor.
        if hasattr(view, 'ui') and view.ui is not None:
            # This makes the control draggable outside of the main window.
            #view_dock_control.export = 'enthought.pyface.workbench.view'
            view_dock_control.dockable = DockableViewElement(
                should_close=True, ui=view.ui
            )

        view_dock_control.on_close = self._on_view_closed

        def on_id_changed():
            view_dock_control.id = view.id
            return

        view.on_trait_change(on_id_changed, 'id')

        def on_name_changed():
            view_dock_control.set_name(view.name)
            return

        view.on_trait_change(on_name_changed, 'name')

        return

    def _set_item_size(self, dock_control, size):
        """ Sets the size of a dock control. """

        window_width, window_height = self.window.control.GetSize()
        width,        height        = size

        if width != -1:
            dock_control.width = int(window_width * width)

        if height != -1:
            dock_control.height = int(window_height * height)

        return

    #### Trait change handlers ################################################

    #### Static ####

    def _window_changed(self, old, new):
        """ Static trait change handler. """

        if old is not None:
            old.on_trait_change(
                self._on_editor_area_size_changed, 'editor_area_size',
                remove=True
            )


        if new is not None:
            new.on_trait_change(
                self._on_editor_area_size_changed, 'editor_area_size',
            )

    #### Dynamic ####

    def _on_editor_area_size_changed(self, new):
        """ Dynamic trait change handler. """

        window_width, window_height = self.window.control.GetSize()

        # Get the dock control that contains the editor dock window.
        control = self._view_dock_window.get_control(self.editor_area_id)

        # We actually resize the region that the editor area is in.
        region = control.parent
        region.width  = int(new[0] * window_width)
        region.height = int(new[1] * window_height)

        return

    #### Dock window handlers #################################################

    # fixme: Should these just fire events that the window listens to?
    def _on_view_closed(self, dock_control, force):
        """ Called when a view is closed via the dock window control. """

        view = self.window.get_view_by_id(dock_control.id)
        if view is not None:
            logger.debug('workbench destroying view control [%s]', view)
            try:
                view.visible = False
                view.destroy_control()

            except:
                logger.exception('error destroying view control [%s]', view)

        return True

    def _on_editor_closed(self, dock_control, force):
        """ Called when an editor is closed via the dock window control. """

        editor = self.window.get_editor_by_id(dock_control.id)
        if editor is not None:
            logger.debug('workbench destroying editor control [%s]', editor)
            try:
                # fixme: We would like this event to be vetoable, but it isn't
                # just yet (we will need to modify the dock window package).
                self.editor_closing = editor
                editor.destroy_control()
                self.editor_closed = editor

            except:
                logger.exception('error destroying editor control[%s]', editor)

            # fixme: Hmmm, brutal reach in to the window here!
            self.window.editors.remove(editor)

        return True

    ###########################################################################
    # 'WorkbenchWindowLayout' toolkit interface.
    ###########################################################################

    def _tk_workbenchwindowlayout_activate_editor(self, editor):
        """ Activates an editor. """

        # This brings the dock control tab to the front.
        self._editor_dock_window.activate_control(editor.id)

        return

    def _tk_workbenchwindowlayout_activate_view(self, view):
        """ Activates a view. """

        # This brings the dock control tab to the front.
        self._view_dock_window.activate_control(view.id)

        return

    def _tk_workbenchwindowlayout_add_editor(self, editor, title):
        """ Adds an editor. """

        # Create a dock control that contains the editor.
        editor_dock_control = self._create_editor_dock_control(editor)

        # If there are no other editors open (i.e., this is the first one!),
        # then create a new region to put the editor in.
        controls = self._editor_dock_window.get_controls()
        if len(controls) == 0:
            # Get a reference to the empty editor section.
            sizer   = self._editor_dock_window.control.GetSizer()
            section = sizer.GetContents()

            # Add a region containing the editor dock control.
            region  = DockRegion(contents=[editor_dock_control])
            section.contents = [region]

        # Otherwise, add the editor to the same region as the first editor
        # control.
        #
        # fixme: We might want a more flexible placement strategy at some
        # point!
        else:
            region = controls[0].parent
            region.add(editor_dock_control)

        # fixme: Without this the window does not draw properly (manually
        # resizing the window makes it better!).
        self._editor_dock_window.update_layout()

        return

    def _tk_workbenchwindowlayout_add_view(self, view, position, relative_to=None, size=(-1, -1)):
        """ Adds a view. """

        # Create a dock control that contains the view.
        dock_control = self._create_view_dock_control(view)

        if position == 'with':
            self._add_view_with(dock_control, relative_to)

        else:
            self._add_view_relative(dock_control, relative_to, position, size)

        return

    def _tk_workbenchwindowlayout_close_editor(self, editor):
        """ Closes an editor. """

        self._editor_dock_window.close_control(editor.id)

        return

    def _tk_workbenchwindowlayout_close(self):
        """ Closes the entire window layout. """

        self._editor_dock_window.close()
        self._view_dock_window.close()

        return

    def _tk_workbenchwindowlayout_create(self):
        """ Create and return the initial window layout. """

        # The view dock window is where all of the views live. It also contains
        # a nested dock window where all of the editors live.
        self._view_dock_window = WorkbenchDockWindow(self.window.control)

        # The editor dock window (which is nested inside the view dock window)
        # is where all of the editors live.
        self._editor_dock_window = WorkbenchDockWindow(
            self._view_dock_window.control
        )
        editor_dock_window_sizer = DockSizer(contents=DockSection())
        self._editor_dock_window.control.SetSizer(editor_dock_window_sizer)

        # Nest the editor dock window in the view dock window.
        editor_dock_window_control = DockControl(
            id      = self.editor_area_id,
            name    = 'Editors',
            control = self._editor_dock_window.control,
            style   = 'fixed',
            width   = self.window.editor_area_size[0],
            height  = self.window.editor_area_size[1],
        )

        view_dock_window_sizer = DockSizer(
            contents=[editor_dock_window_control]
        )

        self._view_dock_window.control.SetSizer(view_dock_window_sizer)

        # FIXME v3: The wx backend doesn't need this at the moment so we leave
        # it until we work out what the proper thing to do is.  Maybe we should
        # return view_dock_window_sizer and the call to SetSizer should be in
        # ApplicationWindow._create() - depends on what other ApplicationWindow
        # sub-classes do.
        return None

    def _tk_workbenchwindowlayout_contains_view(self, view):
        """ Returns True if the view exists in the window layout. """

        return self._view_dock_window.get_control(view.id, False) is not None

    def _tk_workbenchwindowlayout_refresh(self):
        """ Refreshes the window layout to reflect any changes. """

        self._view_dock_window.update_layout()

        return

    def _tk_workbenchwindowlayout_reset_editors(self):
        """ Activates the first editor in every region. """

        self._editor_dock_window.reset_regions()

        return

    def _tk_workbenchwindowlayout_reset_views(self):
        """ Activates the first view in every region. """

        self._view_dock_window.reset_regions()

        return

    def _tk_workbenchwindowlayout_set_editor_area_visible(self, visible):
        """ Sets the editor area visibility. """

        dock_control = self._view_dock_window.get_control(
            self.editor_area_id, visible_only=False
        )
        dock_control.show(visible, layout=True)

        return

    def _tk_workbenchwindowlayout_set_view_visible(self, view, visible):
        """ Sets a view's visibility. """

        dock_control = self._view_dock_window.get_control(
            view.id, visible_only=False
        )
        dock_control.show(visible, layout=True)

        return

    def _tk_workbenchwindowlayout_get_view_memento(self):
        """ Returns the state of the views. """

        structure = self._view_dock_window.get_structure()

        # We always return a clone.
        return cPickle.loads(cPickle.dumps(structure))

    def _tk_workbenchwindowlayout_set_view_memento(self, memento):
        """ Restores the state of the views. """

        # We always use a clone.
        memento = cPickle.loads(cPickle.dumps(memento))

        # The handler knows how to resolve view Ids when setting the dock
        # window structure.
        handler = ViewSetStructureHandler(self)

        # Set the layout of the views.
        self._view_dock_window.set_structure(memento, handler)

        # fixme: We should be able to do this in the handler but we don't get a
        # reference to the actual dock control in 'resolve_id'.
        for view in self.window.views:
            control = self._view_dock_window.get_control(view.id)
            if control is not None:
                self._initialize_view_dock_control(view, control)
                view.visible = control.visible

            else:
                view.visible = False

        return

    def _tk_workbenchwindowlayout_get_editor_memento(self):
        """ Returns the state of the editors. """

        # Get the layout of the editors.
        structure = self._editor_dock_window.get_structure()

        # Get a memento to every editor.
        editor_references = self._get_editor_references()

        return (structure, editor_references)

    def _tk_workbenchwindowlayout_set_editor_memento(self, memento):
        """ Restores the state of the editors. """

        # fixme: Mementos might want to be a bit more formal than tuples!
        structure, editor_references = memento

        if len(structure.contents) > 0:
            # The handler knows how to resolve editor Ids when setting the dock
            # window structure.
            handler = EditorSetStructureHandler(self, editor_references)

            # Set the layout of the editors.
            self._editor_dock_window.set_structure(structure, handler)

            # fixme: We should be able to do this in the handler but we don't
            # get a reference to the actual dock control in 'resolve_id'.
            for editor in self.window.editors:
                control = self._editor_dock_window.get_control(editor.id)
                if control is not None:
                    self._initialize_editor_dock_control(editor, control)

        return

#### EOF ######################################################################
