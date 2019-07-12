# Standard library imports.
import sys

# Enthought library imports.
from pyface.tasks.i_editor_area_pane import IEditorAreaPane, \
    MEditorAreaPane
from traits.api import Bool, cached_property, Callable, Dict, Instance, List, \
    on_trait_change, Property, provides, Str
from pyface.qt import is_qt4, QtCore, QtGui
from pyface.action.api import Action, Group, MenuManager
from pyface.tasks.task_layout import PaneItem, Tabbed, Splitter
from pyface.mimedata import PyMimeData
from pyface.api import FileDialog
from pyface.constant import OK
from pyface.drop_handler import IDropHandler, BaseDropHandler, FileDropHandler

# Local imports.
from .task_pane import TaskPane

###############################################################################
# 'SplitEditorAreaPane' class.
###############################################################################

@provides(IEditorAreaPane)
class SplitEditorAreaPane(TaskPane, MEditorAreaPane):
    """ The toolkit-specific implementation of an SplitEditorAreaPane.

    See the IEditorAreaPane interface for API documentation.
    """


    #### SplitEditorAreaPane interface #####################################

    # Currently active tabwidget
    active_tabwidget = Instance(QtGui.QTabWidget)

    # list of installed drop handlers
    drop_handlers = List(IDropHandler)

    # Additional callback functions. Few useful callbacks that can be included:
    #  'new': new file action (takes no argument)
    #  'open': open file action (takes file_path as single argument)
    #  'open_dialog': show the open file dialog (responsibility of the callback,
    #     takes no argument), overrides 'open' callback
    # They are used to create shortcut buttons for these actions in the empty
    # pane that gets created when the user makes a split
    callbacks = Dict({}, key=Str, value=Callable)

    # The constructor of the empty widget which comes up when one creates a split
    create_empty_widget = Callable

    #### Private interface ###################################################

    _private_drop_handlers = List(IDropHandler)
    _all_drop_handlers = Property(
        List(IDropHandler),
        depends_on=['drop_handlers', '_private_drop_handlers']
    )

    def __private_drop_handlers_default(self):
        """ By default, two private drop handlers are installed:

            1. For dropping of tabs from one pane to other
            2. For dropping of supported files from file-browser pane or outside
            the application
        """
        return [TabDropHandler(),
                FileDropHandler(extensions=self.file_drop_extensions,
                                open_file=lambda path:self.trait_set(file_dropped=path))]

    @cached_property
    def _get__all_drop_handlers(self):
        return self.drop_handlers + self._private_drop_handlers

    def _create_empty_widget_default(self):
        return lambda : self.active_tabwidget.create_empty_widget()

    ###########################################################################
    # 'TaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        # Create and configure the Editor Area Widget.
        self.control = EditorAreaWidget(self, parent)
        self.active_tabwidget = self.control.tabwidget()

        # handle application level focus changes
        QtGui.QApplication.instance().focusChanged.connect(self._focus_changed)

        # set key bindings
        self.set_key_bindings()

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """
        # disconnect application level focus change signals first, else it gives
        # weird runtime errors trying to access non-existent objects
        QtGui.QApplication.instance().focusChanged.disconnect(self._focus_changed)

        for editor in self.editors[:]:
            self.remove_editor(editor)

        super(SplitEditorAreaPane, self).destroy()

    ###########################################################################
    # 'IEditorAreaPane' interface.
    ###########################################################################

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """
        active_tabwidget = editor.control.parent().parent()
        active_tabwidget.setCurrentWidget(editor.control)
        self.active_tabwidget = active_tabwidget
        editor_widget = editor.control.parent()
        editor_widget.setVisible(True)
        editor_widget.raise_()
        # Set focus on last active widget in editor if possible
        if editor.control.focusWidget():
            editor.control.focusWidget().setFocus()
        else:
            editor.control.setFocus()
        # Set active_editor at the end of the method so that the notification
        # occurs when everything is ready.
        self.active_editor = editor

    def add_editor(self, editor):
        """ Adds an editor to the active_tabwidget
        """
        editor.editor_area = self
        editor.create(self.active_tabwidget)
        index = self.active_tabwidget.addTab(editor.control,
                                             self._get_label(editor))
        # There seem to be a bug in pyside or qt, where the index is set to 1
        # when you create the first tab. This is a hack to fix it.
        if self.active_tabwidget.count() == 1:
            index = 0
        self.active_tabwidget.setTabToolTip(index, editor.tooltip)
        self.editors.append(editor)

    def remove_editor(self, editor):
        """ Removes an editor from the associated tabwidget
        """
        tabwidget = editor.control.parent().parent()
        tabwidget.removeTab(tabwidget.indexOf(editor.control))
        self.editors.remove(editor)
        editor.destroy()
        editor.editor_area = None
        if not self.editors:
            self.active_editor = None


    ##########################################################################
    # 'IAdvancedEditorAreaPane' interface.
    ##########################################################################

    def get_layout(self):
        """ Returns a LayoutItem that reflects the current state of the
        tabwidgets in the split framework.
        """
        return self.control.get_layout()

    def set_layout(self, layout):
        """ Applies the given LayoutItem.
        """
        self.control.set_layout(layout)

    ##########################################################################
    # 'SplitEditorAreaPane' interface.
    ##########################################################################

    def get_context_menu(self, pos):
        """ Returns a context menu containing split/collapse actions

        pos : position (in global coordinates) where the context menu was
        requested
        """
        menu = MenuManager()
        splitter = None

        splitter = None
        for tabwidget in self.tabwidgets():
            # obtain tabwidget's bounding rectangle in global coordinates
            global_rect = QtCore.QRect(tabwidget.mapToGlobal(QtCore.QPoint(0, 0)),
                                        tabwidget.size())
            if global_rect.contains(pos):
                splitter = tabwidget.parent()

        # no split/collapse context menu for positions outside any tabwidget
        # region
        if not splitter:
            return

        # add split actions (only show for non-empty tabwidgets)
        if not splitter.is_empty():
            actions = [Action(id='split_hor', name='Create new pane to the right',
                       on_perform=lambda : splitter.split(orientation=
                        QtCore.Qt.Horizontal)),
                       Action(id='split_ver', name='Create new pane to the bottom',
                       on_perform=lambda : splitter.split(orientation=
                        QtCore.Qt.Vertical))]

            splitgroup = Group(*actions, id='split')
            menu.append(splitgroup)

        # add collapse action (only show for collapsible splitters)
        if splitter.is_collapsible():
            if splitter is splitter.parent().leftchild:
                if splitter.parent().orientation() == QtCore.Qt.Horizontal:
                    text = 'Merge with right pane'
                else:
                    text = 'Merge with bottom pane'
            else:
                if splitter.parent().orientation() == QtCore.Qt.Horizontal:
                    text = 'Merge with left pane'
                else:
                    text = 'Merge with top pane'
            actions = [Action(id='merge', name=text,
                        on_perform=lambda : splitter.collapse())]

            collapsegroup = Group(*actions, id='collapse')
            menu.append(collapsegroup)

        # return QMenu object
        return menu

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_label(self, editor):
        """ Return a tab label for an editor.
        """
        try:
            label = editor.name
            if editor.dirty:
                label = '*' + label
        except AttributeError:
            label = ''
        return label

    def _get_editor(self, editor_widget):
        """ Returns the editor corresponding to editor_widget
        """
        for editor in self.editors:
            if editor.control is editor_widget:
                return editor
        return None

    def set_key_bindings(self):
        """ Set keyboard shortcuts for tabbed navigation
        """
        # Add shortcuts for scrolling through tabs.
        if sys.platform == 'darwin':
            next_seq = 'Ctrl+}'
            prev_seq = 'Ctrl+{'
        else:
            next_seq = 'Ctrl+PgDown'
            prev_seq = 'Ctrl+PgUp'
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(next_seq), self.control)
        shortcut.activated.connect(self._next_tab)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(prev_seq), self.control)
        shortcut.activated.connect(self._previous_tab)

        # Add shortcuts for switching to a specific tab.
        mod = 'Ctrl+' if sys.platform == 'darwin' else 'Alt+'
        mapper = QtCore.QSignalMapper(self.control)
        mapper.mapped.connect(self._activate_tab)
        for i in range(1, 10):
            sequence = QtGui.QKeySequence(mod + str(i))
            shortcut = QtGui.QShortcut(sequence, self.control)
            shortcut.activated.connect(mapper.map)
            mapper.setMapping(shortcut, i - 1)

    def _activate_tab(self, index):
        """ Activates the tab with the specified index, if there is one.
        """
        self.active_tabwidget.setCurrentIndex(index)
        current_widget = self.active_tabwidget.currentWidget()
        for editor in self.editors:
            if current_widget == editor.control:
                self.activate_editor(editor)

    def _next_tab(self):
        """ Activate the tab after the currently active tab.
        """
        index = self.active_tabwidget.currentIndex()
        new_index = index + 1 if index < self.active_tabwidget.count() - 1 else 0
        self._activate_tab(new_index)

    def _previous_tab(self):
        """ Activate the tab before the currently active tab.
        """
        index = self.active_tabwidget.currentIndex()
        new_index = index - 1 if index > 0  else self.active_tabwidget.count() - 1
        self._activate_tab(new_index)

    def tabwidgets(self):
        """ Returns the list of tabwidgets associated with the current editor
        area.
        """
        return self.control.tabwidgets()

    #### Trait change handlers ################################################

    @on_trait_change('editors:[dirty, name]')
    def _update_label(self, editor, name, new):
        index = self.active_tabwidget.indexOf(editor.control)
        self.active_tabwidget.setTabText(index, self._get_label(editor))

    @on_trait_change('editors:tooltip')
    def _update_tooltip(self, editor, name, new):
        index = self.active_tabwidget.indexOf(editor.control)
        self.active_tabwidget.setTabToolTip(index, self._get_label(editor))

    #### Signal handlers ######################################################

    def _find_ancestor_draggable_tab_widget(self, control):
        """ Find the draggable tab widget to which a widget belongs. """

        while not isinstance(control, DraggableTabWidget):
            control = control.parent()

        return control

    def _focus_changed(self, old, new):
        """Set the active tabwidget after an application-level change in focus.
        """

        if new is not None:
            if isinstance(new, DraggableTabWidget):
                if new.editor_area == self:
                    self.active_tabwidget = new
            elif isinstance(new, QtGui.QTabBar):
                if self.control.isAncestorOf(new):
                    self.active_tabwidget = \
                        self._find_ancestor_draggable_tab_widget(new)
            else:
                # Check if any of the editor widgets have focus.
                # If so, make it active.
                for editor in self.editors:
                    control = editor.control
                    if control is not None and control.isAncestorOf(new):
                        active_tabwidget = \
                            self._find_ancestor_draggable_tab_widget(control)
                        active_tabwidget.setCurrentWidget(control)
                        self.active_tabwidget = active_tabwidget
                        break

    def _active_tabwidget_changed(self, new):
        """Set the active editor whenever the active tabwidget updates.
        """

        if new is None or new.parent().is_empty():
            active_editor = None
        else:
            active_editor = self._get_editor(new.currentWidget())

        self.active_editor = active_editor


###############################################################################
# Auxiliary classes.
###############################################################################

class EditorAreaWidget(QtGui.QSplitter):
    """ Container widget to hold a QTabWidget which are separated by other
    QTabWidgets via splitters.

    An EditorAreaWidget is essentially a Node object in the editor area layout
    tree.
    """

    def __init__(self, editor_area, parent=None, tabwidget=None):
        """ Creates an EditorAreaWidget object.

        editor_area : global SplitEditorAreaPane instance
        parent : parent splitter
        tabwidget : tabwidget object contained by this splitter

        """
        super(EditorAreaWidget, self).__init__(parent=parent)
        self.editor_area = editor_area

        if not tabwidget:
            tabwidget = DraggableTabWidget(editor_area=self.editor_area,
                                        parent=self)

        # add the tabwidget to the splitter
        self.addWidget(tabwidget)
        # showing the tabwidget after reparenting
        tabwidget.show()

        # Initializes left and right children to None (since no initial splitter
        # children are present)
        self.leftchild = None
        self.rightchild = None

    def get_layout(self):
        """ Returns a LayoutItem that reflects the layout of the current
        splitter.
        """
        ORIENTATION_MAP = {QtCore.Qt.Horizontal: 'horizontal',
                           QtCore.Qt.Vertical: 'vertical'}
        # obtain layout based on children layouts
        if not self.is_leaf():
            layout = Splitter(self.leftchild.get_layout(),
                            self.rightchild.get_layout(),
                            orientation=ORIENTATION_MAP[self.orientation()])
        # obtain the Tabbed layout
        else:
            if self.is_empty():
                layout = Tabbed(PaneItem(id=-1,
                                        width=self.width(),
                                        height=self.height()),
                                active_tab=0)
            else:
                items = []
                for i in range(self.tabwidget().count()):
                    widget = self.tabwidget().widget(i)
                    # mark identification for empty_widget
                    editor = self.editor_area._get_editor(widget)
                    item_id = self.editor_area.editors.index(editor)
                    item_width = self.width()
                    item_height = self.height()
                    items.append(PaneItem(id=item_id,
                                        width=item_width,
                                        height=item_height))
                layout = Tabbed(*items, active_tab=self.tabwidget().currentIndex())
        return layout

    def set_layout(self, layout):
        """ Applies the given LayoutItem to current splitter.
        """
        ORIENTATION_MAP = {'horizontal': QtCore.Qt.Horizontal,
                           'vertical': QtCore.Qt.Vertical}
        # if not a leaf splitter
        if isinstance(layout, Splitter):
            self.split(orientation=ORIENTATION_MAP[layout.orientation])
            self.leftchild.set_layout(layout=layout.items[0])
            self.rightchild.set_layout(layout=layout.items[1])

            # setting sizes of children along splitter direction
            if layout.orientation=='horizontal':
                sizes = [self.leftchild.width(), self.rightchild.width()]
                self.resize(sum(sizes), self.leftchild.height())
            else:
                sizes = [self.leftchild.height(), self.rightchild.height()]
                self.resize(self.leftchild.width(), sum(sizes))
            self.setSizes(sizes)

        # if it is a leaf splitter
        elif isinstance(layout, Tabbed):
            # don't clear-out empty_widget's information if all it contains is an
            # empty_widget
            if not self.is_empty():
                self.tabwidget().clear()

            for item in layout.items:
                if not item.id==-1:
                    editor = self.editor_area.editors[item.id]
                    self.tabwidget().addTab(editor.control,
                                            self.editor_area._get_label(editor))
                self.resize(item.width, item.height)
            self.tabwidget().setCurrentIndex(layout.active_tab)

    def tabwidget(self):
        """ Obtain the tabwidget associated with current EditorAreaWidget
        (returns None for non-leaf splitters)
        """
        for child in self.children():
            if isinstance(child, QtGui.QTabWidget):
                return child
        return None

    def tabwidgets(self):
        """ Return a list of tabwidgets associated with current splitter or
        any of its descendants.
        """
        tabwidgets = []
        if self.is_leaf():
            tabwidgets.append(self.tabwidget())

        else:
            tabwidgets.extend(self.leftchild.tabwidgets())
            tabwidgets.extend(self.rightchild.tabwidgets())

        return tabwidgets

    def sibling(self):
        """ Returns another child of its parent. Returns None if it can't find
        any sibling.
        """
        parent = self.parent()

        if self.is_root():
            return None

        if self is parent.leftchild:
            return parent.rightchild
        elif self is parent.rightchild:
            return parent.leftchild

    def is_root(self):
        """ Returns True if the current EditorAreaWidget is the root widget.
        """
        parent = self.parent()
        if isinstance(parent, EditorAreaWidget):
            return False
        else:
            return True

    def is_leaf(self):
        """ Returns True if the current EditorAreaWidget is a leaf, i.e., it has
        a tabwidget as one of it's immediate child.
        """
        # a leaf has it's leftchild and rightchild None
        if not self.leftchild and not self.rightchild:
            return True
        return False

    def is_empty(self):
        """ Returns True if the current splitter's tabwidget doesn't contain any
        tab.
        """
        return bool(self.tabwidget().empty_widget)

    def is_collapsible(self):
        """ Returns True if the current splitter can be collapsed to its sibling,
        i.e. if it is (a) either empty, or (b) it has a sibling which is a leaf.
        """
        if self.is_root():
            return False

        if self.is_empty():
            return True

        sibling = self.sibling()

        if sibling.is_leaf():
            return True
        else:
            return False

    def split(self, orientation=QtCore.Qt.Horizontal):
        """ Split the current splitter into two children splitters. The current
        splitter's tabwidget is moved to the left child while a new empty
        tabwidget is added to the right child.

        orientation : whether to split horizontally or vertically
        """
        # set splitter orientation
        self.setOrientation(orientation)
        orig_size = self.sizes()[0]

        # create new children
        self.leftchild = EditorAreaWidget(self.editor_area, parent=self,
                                        tabwidget=self.tabwidget())
        self.rightchild = EditorAreaWidget(self.editor_area, parent=self,
                                        tabwidget=None)

        # add newly generated children
        self.addWidget(self.leftchild)
        self.addWidget(self.rightchild)

        # set equal sizes of splits
        self.setSizes([orig_size/2,orig_size/2])

        # make the rightchild's tabwidget active & show its empty widget
        self.editor_area.active_tabwidget = self.rightchild.tabwidget()

    def collapse(self):
        """ Collapses the current splitter and its sibling splitter to their
        parent splitter. Merges together the tabs of both's tabwidgets.

        Does nothing if the current splitter is not collapsible.
        """
        if not self.is_collapsible():
            return

        parent = self.parent()
        sibling = self.sibling()

        # this will happen only if self is empty, else it will not be
        # collapsible at all
        if sibling and (not sibling.is_leaf()):
            parent.setOrientation(sibling.orientation())
            # reparent sibling's children to parent
            parent.addWidget(sibling.leftchild)
            parent.addWidget(sibling.rightchild)
            parent.leftchild = sibling.leftchild
            parent.rightchild = sibling.rightchild
            # blindly make the first tabwidget active as it is not clear which
            # tabwidget should get focus now (FIXME??)
            self.editor_area.active_tabwidget = parent.tabwidgets()[0]
            self.setParent(None)
            sibling.setParent(None)
            return

        # save original currentwidget to make active later
        # (if self is empty, make the currentwidget of sibling active)
        if not self.is_empty():
            orig_currentWidget = self.tabwidget().currentWidget()
        else:
            orig_currentWidget = sibling.tabwidget().currentWidget()

        left = parent.leftchild.tabwidget()
        right = parent.rightchild.tabwidget()
        target = DraggableTabWidget(editor_area=self.editor_area, parent=parent)

        # add tabs of left and right tabwidgets to target
        for source in (left, right):
            # Note: addTab removes widgets from source tabwidget, so
            # grabbing all the source widgets beforehand
            # (not grabbing empty_widget)
            widgets = [source.widget(i) for i in range(source.count()) if not
                        source.widget(i) is source.empty_widget]
            for editor_widget in widgets:
                editor = self.editor_area._get_editor(editor_widget)
                target.addTab(editor_widget,
                            self.editor_area._get_label(editor))

        # add target to parent
        parent.addWidget(target)

        # make target the new active tabwidget and make the original focused
        # widget active in the target too
        self.editor_area.active_tabwidget = target
        target.setCurrentWidget(orig_currentWidget)

        # remove parent's splitter children
        parent.leftchild = None
        parent.rightchild = None
        self.setParent(None)
        sibling.setParent(None)


class DraggableTabWidget(QtGui.QTabWidget):
    """ Implements a QTabWidget with event filters for tab drag and drop
    """

    def __init__(self, editor_area, parent):
        """
        editor_area : global SplitEditorAreaPane instance
        parent : parent of the tabwidget
        """
        super(DraggableTabWidget, self).__init__(parent)
        self.editor_area = editor_area

        # configure QTabWidget
        self.setTabBar(DraggableTabBar(editor_area=editor_area, parent=self))
        self.setDocumentMode(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusProxy(None)
        self.setMovable(False) # handling move events myself
        self.setTabsClosable(True)
        self.setAutoFillBackground(True)

        # set drop and context menu policies
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        # connecting signals
        self.tabCloseRequested.connect(self._close_requested)
        self.currentChanged.connect(self._current_changed)

        # shows the custom empty widget containing buttons for relevant actions
        self.show_empty_widget()

    def show_empty_widget(self):
        """ Shows the empty widget (containing buttons to open new file, and
        collapse the split).
        """
        self.empty_widget = None
        self.editor_area.active_tabwidget = self

        # callback to editor_area's public `create_empty_widget` Callable trait
        empty_widget = self.editor_area.create_empty_widget()

        self.addTab(empty_widget, '')
        self.empty_widget = empty_widget
        self.setFocus()

        # don't allow tab closing if empty widget comes up on a root tabwidget
        if self.parent().is_root():
            self.setTabsClosable(False)

        self.setTabText(0, '     ')

    def hide_empty_widget(self):
        """ Hides the empty widget (containing buttons to open new file, and
        collapse the split) based on whether the tabwidget is empty or not.
        """
        index = self.indexOf(self.empty_widget)
        self.removeTab(index)
        self.empty_widget.deleteLater()
        self.empty_widget = None
        self.setTabsClosable(True)

    def create_empty_widget(self):
        """ Creates the QFrame object to be shown when the current tabwidget is
        empty.
        """
        frame = QtGui.QFrame(parent=self)
        frame.setFrameShape(QtGui.QFrame.StyledPanel)
        layout = QtGui.QVBoxLayout(frame)

        # Add new file button and open file button only if the `callbacks` trait
        # of the editor_area has a callable for key `new` and key `open`
        new_file_action = self.editor_area.callbacks.get('new', None)
        open_file_action = self.editor_area.callbacks.get('open_dialog', None)
        open_show_dialog = False
        if open_file_action is None:
            open_file_action = self.editor_area.callbacks.get('open', None)
            open_show_dialog = True
        if not (new_file_action and open_file_action):
            return frame

        layout.addStretch()

        # generate new file button
        newfile_btn = QtGui.QPushButton('Create a new file', parent=frame)
        newfile_btn.clicked.connect(new_file_action)
        layout.addWidget(newfile_btn, alignment=QtCore.Qt.AlignHCenter)

        # generate label
        label = QtGui.QLabel(parent=frame)
        label.setText("""<span style='font-size:14px; color:#999999'>
                        or
                        </span>""")
        layout.addWidget(label, alignment=QtCore.Qt.AlignHCenter)

        # generate open button
        open_btn = QtGui.QPushButton('Select files from your computer', parent=frame)
        def _open():
            if open_show_dialog:
                open_dlg = FileDialog(action='open')
                open_dlg.open()
                self.editor_area.active_tabwidget = self
                if open_dlg.return_code == OK:
                    open_file_action(open_dlg.path)
            else:
                open_file_action()
        open_btn.clicked.connect(_open)
        layout.addWidget(open_btn, alignment=QtCore.Qt.AlignHCenter)

        # generate label
        label = QtGui.QLabel(parent=frame)
        label.setText("""<span style='font-size:14px; color:#999999'>
                        Tip: You can also drag and drop files/tabs here.
                        </span>""")
        layout.addWidget(label, alignment=QtCore.Qt.AlignHCenter)

        layout.addStretch()
        frame.setLayout(layout)

        return frame

    def get_names(self):
        """ Utility function to return names of all the editors open in the
        current tabwidget.
        """
        names = []
        for i in range(self.count()):
            editor_widget = self.widget(i)
            editor = self.editor_area._get_editor(editor_widget)
            if editor:
                names.append(editor.name)
        return names

    ###### Signal handlers ####################################################

    def _close_requested(self, index):
        """ Re-implemented to close the editor when it's tab is closed
        """
        widget = self.widget(index)

        # if close requested on empty_widget, collapse the pane and return
        if widget is self.empty_widget:
            self.parent().collapse()
            return
        editor = self.editor_area._get_editor(widget)
        editor.close()

    def _current_changed(self, index):
        """Re-implemented to update active editor
        """
        self.setCurrentIndex(index)
        editor_widget = self.widget(index)
        self.editor_area.active_editor = self.editor_area._get_editor(editor_widget)

    def tabInserted(self, index):
        """ Re-implemented to hide empty_widget when adding a new widget
        """
        # sets tab tooltip only if a real editor was added (not an empty_widget)
        editor = self.editor_area._get_editor(self.widget(index))
        if editor:
            self.setTabToolTip(index, editor.tooltip)

        if self.empty_widget:
            self.hide_empty_widget()

    def tabRemoved(self, index):
        """ Re-implemented to show empty_widget again if all tabs are removed
        """
        if not self.count() and not self.empty_widget:
            self.show_empty_widget()

    ##### Event handlers ######################################################

    def contextMenuEvent(self, event):
        """ To show collapse context menu even on empty tabwidgets
        """
        local_pos = event.pos()
        if (self.empty_widget is not None or
                self.tabBar().rect().contains(local_pos)):
            # Only display if we are in the tab bar region or the whole area if
            # we are displaying the default empty widget.
            global_pos = self.mapToGlobal(local_pos)
            menu = self.editor_area.get_context_menu(pos=global_pos)
            qmenu = menu.create_menu(self)
            qmenu.exec_(global_pos)

    def dragEnterEvent(self, event):
        """ Re-implemented to highlight the tabwidget on drag enter
        """
        for handler in self.editor_area._all_drop_handlers:
            if handler.can_handle_drop(event, self):
                self.editor_area.active_tabwidget = self
                self.setBackgroundRole(QtGui.QPalette.Highlight)
                event.acceptProposedAction()
                return

        super(DraggableTabWidget, self).dragEnterEvent(event)

    def dropEvent(self, event):
        """ Re-implemented to handle drop events
        """
        for handler in self.editor_area._all_drop_handlers:
            if handler.can_handle_drop(event, self):
                handler.handle_drop(event, self)
                self.setBackgroundRole(QtGui.QPalette.Window)
                event.acceptProposedAction()
                break

    def dragLeaveEvent(self, event):
        """ Clear widget highlight on leaving
        """
        self.setBackgroundRole(QtGui.QPalette.Window)
        return super(DraggableTabWidget, self).dragLeaveEvent(event)


class DraggableTabBar(QtGui.QTabBar):
    """ Implements a QTabBar with event filters for tab drag
    """
    def __init__(self, editor_area, parent):
        super(DraggableTabBar, self).__init__(parent)
        self.editor_area = editor_area
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.drag_obj = None

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            index = self.tabAt(event.pos())
            tabwidget = self.parent()
            if tabwidget.widget(index) and (not tabwidget.widget(index) == tabwidget.empty_widget):
                self.drag_obj = TabDragObject(start_pos=event.pos(), tabBar=self)
        return super(DraggableTabBar, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ Re-implemented to create a drag event when the mouse is moved for a
        sufficient distance while holding down mouse button.
        """
        # go into the drag logic only if a drag_obj is active
        if self.drag_obj:
            # is the left mouse button still pressed?
            if not event.buttons()==QtCore.Qt.LeftButton:
                pass
            # has the mouse been dragged for sufficient distance?
            elif ((event.pos() - self.drag_obj.start_pos).manhattanLength()
                < QtGui.QApplication.startDragDistance()):
                pass
            # initiate drag
            else:
                drag = QtGui.QDrag(self.drag_obj.widget)
                mimedata = PyMimeData(data=self.drag_obj, pickle=False)
                drag.setPixmap(self.drag_obj.get_pixmap())
                drag.setHotSpot(self.drag_obj.get_hotspot())
                drag.setMimeData(mimedata)
                drag.exec_()
                self.drag_obj = None # deactivate the drag_obj again
                return
        return super(DraggableTabBar, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """ Re-implemented to deactivate the drag when mouse button is
        released
        """
        self.drag_obj = None
        return super(DraggableTabBar, self).mouseReleaseEvent(event)


class TabDragObject(object):
    """ Class to hold information related to tab dragging/dropping
    """

    def __init__(self, start_pos, tabBar):
        """
        Parameters
        ----------

        start_pos : position in tabBar coordinates where the drag was started
        tabBar : tabBar containing the tab on which drag started
        """
        self.start_pos = start_pos
        self.from_index = tabBar.tabAt(self.start_pos)
        self.from_editor_area = tabBar.parent().editor_area
        self.widget = tabBar.parent().widget(self.from_index)
        self.from_tabbar = tabBar

    def get_pixmap(self):
        """ Returns the drag pixmap including page widget and tab rectangle.
        """
        # instatiate the painter object with gray-color filled pixmap
        tabBar = self.from_tabbar
        tab_rect = tabBar.tabRect(self.from_index)
        size = self.widget.rect().size()
        result_pixmap = QtGui.QPixmap(size)
        painter = QtGui.QStylePainter(result_pixmap, tabBar)

        painter.fillRect(result_pixmap.rect(), QtCore.Qt.lightGray)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)

        optTabBase = QtGui.QStyleOptionTabBarBase()
        optTabBase.initFrom(tabBar)
        painter.drawPrimitive(QtGui.QStyle.PE_FrameTabBarBase, optTabBase)

        # region of active tab
        if is_qt4:  # grab wasn't introduced until Qt5
            pixmap1 = QtGui.QPixmap.grabWidget(tabBar, tab_rect)
        else:
            pixmap1 = tabBar.grab(tab_rect)

        painter.drawPixmap(0, 0, pixmap1)

        # region of the page widget
        if is_qt4:
            pixmap2 = QtGui.QPixmap.grabWidget(self.widget)
        else:
            pixmap2 = self.widget.grab()
        painter.drawPixmap(0, tab_rect.height(), size.width(), size.height(), pixmap2)

        # finish painting
        painter.end()

        return result_pixmap

    def get_hotspot(self):
        return self.start_pos - self.from_tabbar.tabRect(self.from_index).topLeft()

###############################################################################
# Default drop handlers.
###############################################################################

class TabDropHandler(BaseDropHandler):
    """ Class to handle tab drop events
    """

    # whether to allow dragging of tabs across different opened windows
    allow_cross_window_drop = Bool(False)

    def can_handle_drop(self, event, target):
        if isinstance(event.mimeData(), PyMimeData) and \
            isinstance(event.mimeData().instance(), TabDragObject):
            if not self.allow_cross_window_drop:
                drag_obj = event.mimeData().instance()
                return drag_obj.from_editor_area == target.editor_area
            else:
                return True
        return False

    def handle_drop(self, event, target):
        # get the drop object back
        drag_obj = event.mimeData().instance()

        # extract widget label
        # (editor_area is common to both source and target in most cases but when
        # the dragging happens across different windows, they are not, and hence it
        # must be pulled in directly from the source)
        editor = target.editor_area._get_editor(drag_obj.widget)
        label = target.editor_area._get_label(editor)

        # if drop occurs at a tab bar, insert the tab at that position
        if not target.tabBar().tabAt(event.pos())==-1:
            index = target.tabBar().tabAt(event.pos())
            target.insertTab(index, drag_obj.widget, label)

        else:
            # if the drag initiated from the same tabwidget, put the tab
            # back at the original index
            if target is drag_obj.from_tabbar.parent():
                target.insertTab(drag_obj.from_index, drag_obj.widget, label)
            # else, just add it at the end
            else:
                target.addTab(drag_obj.widget, label)

        # make the dropped widget active
        target.setCurrentWidget(drag_obj.widget)
