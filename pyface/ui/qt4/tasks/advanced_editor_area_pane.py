# Standard library imports.
import sys

# Enthought library imports.
from pyface.tasks.i_editor_area_pane import IEditorAreaPane, \
    MEditorAreaPane
from traits.api import implements, on_trait_change, Instance, Tuple, Callable
from pyface.qt import QtCore, QtGui
from pyface.action.api import Action, Group
from pyface.tasks.task_layout import PaneItem, Tabbed, Splitter
from traitsui.api import Menu
from traitsui.qt4.clipboard import PyMimeData
from pyface.api import FileDialog
from pyface.constant import OK, CANCEL

# Local imports.
from task_pane import TaskPane

###############################################################################
# 'AdvancedEditorAreaPane' class.
###############################################################################

class AdvancedEditorAreaPane(TaskPane, MEditorAreaPane):
    """ The toolkit-specific implementation of an AdvancedEditorAreaPane.

    See the IEditorAreaPane interface for API documentation.
    """

    implements(IEditorAreaPane)

    #### AdvancedEditorAreaPane interface #####################################

    # Currently active tabwidget
    active_tabwidget = Instance(QtGui.QTabWidget)

    # Callable to tell whether the editor task can handle a given object
    can_handle = Callable(lambda obj: None)

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
        self._drag_info = Tuple(enabled=False, start_pos=-1, from_index=-1,
                        drag_widget=None, from_tabwidget=None, pixmap=None)

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

        for editor in self.editors:
            self.remove_editor(editor)

        super(AdvancedEditorAreaPane, self).destroy()

    ###########################################################################
    # 'IEditorAreaPane' interface.
    ###########################################################################

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """
        self.active_editor = editor
        self.active_tabwidget = editor.control.parent().parent()
        self.active_tabwidget.setCurrentWidget(editor.control)
        
    def add_editor(self, editor):
        """ Adds an editor to the active_tabwidget
        """
        editor.editor_area = self
        editor.create(self.active_tabwidget)
        self.editors.append(editor)
        self.active_tabwidget.addTab(editor.control, 
                                    self._get_label(editor))

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
    # 'AdvancedEditorAreaPane' interface.
    ##########################################################################

    def get_context_menu(self, pos):
        """ Returns a context menu containing split/collapse actions

        pos : position (in global coordinates) where the context menu was 
        requested
        """
        menu = Menu()

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
                if splitter.parent().orientation() is QtCore.Qt.Horizontal:
                    text = 'Merge with right pane'
                else:
                    text = 'Merge with bottom pane'
            else:
                if splitter.parent().orientation() is QtCore.Qt.Horizontal:
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

    def _get_dragpixmap(self):
        """ Returns the drag pixmap including page widget and tab rectangle. 
        Returns None if no drag is active.
        """
        if not self._drag_info.enabled:
            return

        drag_widget = self._drag_info.drag_widget
        index = self._drag_info.from_index
        tabwidget = self._drag_info.from_tabwidget

        # instatiate the painter object with gray-color filled pixmap
        result_pixmap = QtGui.QPixmap(tabwidget.rect().size())
        self.painter = QtGui.QPainter(result_pixmap)
        self.painter.fillRect(result_pixmap.rect(), QtCore.Qt.lightGray)
        self.painter.setCompositionMode(QtGui.QPainter.CompositionMode_SourceOver)
        
        # region of active tab
        tab_rect = tabwidget.tabBar().tabRect(index)
        pixmap1 = QtGui.QPixmap.grabWidget(tabwidget.tabBar(), tab_rect)
        self.painter.drawPixmap(0, 0, pixmap1)

        # region of the page widget
        pixmap2 = QtGui.QPixmap.grabWidget(drag_widget)
        self.painter.drawPixmap(0, tab_rect.height(), pixmap2)
        
        # finish painting
        self.painter.end()

        return result_pixmap


    def set_key_bindings(self):
        """ Set keyboard shortcuts for tabbed navigation
        """
        # Add shortcuts for scrolling through tabs.
        if sys.platform == 'darwin':
            next_seq = 'Ctrl+}'
            prev_seq = 'Ctrl+{'
        elif sys.platform.startswith('linux'):
            next_seq = 'Ctrl+PgDown'
            prev_seq = 'Ctrl+PgUp'
        else:
            next_seq = 'Alt+n'
            prev_seq = 'Alt+p'
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(next_seq), self.control)
        shortcut.activated.connect(self._next_tab)
        shortcut = QtGui.QShortcut(QtGui.QKeySequence(prev_seq), self.control)
        shortcut.activated.connect(self._previous_tab)

        # Add shortcuts for switching to a specific tab.
        mod = 'Ctrl+' if sys.platform == 'darwin' else 'Alt+'
        mapper = QtCore.QSignalMapper(self.control)
        mapper.mapped.connect(self._activate_tab)
        for i in xrange(1, 10):
            sequence = QtGui.QKeySequence(mod + str(i))
            shortcut = QtGui.QShortcut(sequence, self.control)
            shortcut.activated.connect(mapper.map)
            mapper.setMapping(shortcut, i - 1)

    def _activate_tab(self, index):
        """ Activates the tab with the specified index, if there is one.
        """
        self.active_tabwidget.setCurrentIndex(index)

    def _next_tab(self):
        """ Activate the tab after the currently active tab.
        """
        index = self.active_tabwidget.currentIndex()
        new_index = index + 1 if index < self.active_tabwidget.count() - 1 else 0
        self.active_tabwidget.setCurrentIndex(new_index)

    def _previous_tab(self):
        """ Activate the tab before the currently active tab.
        """
        index = self.active_tabwidget.currentIndex()
        new_index = index - 1 if index > 0  else self.active_tabwidget.count() - 1
        self.active_tabwidget.setCurrentIndex(new_index)

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

    def _focus_changed(self, old, new):
        """ Handle an application-level focus change to set the active_tabwidget
        """
        if new:
            if isinstance(new, DraggableTabWidget):
                self.active_tabwidget = new
            elif isinstance(new, QtGui.QTabBar):
                self.active_tabwidget = new.parent()
            else:
                # check if any of the editor widgets (or their focus proxies) 
                # have focus. If yes, make it active
                for editor in self.editors:
                    # hasFocus is True if control or it's focusproxy has focus
                    if editor.control.hasFocus():
                        self.activate_editor(editor)
                        break


###############################################################################
# Auxillary classes.
###############################################################################

class EditorAreaWidget(QtGui.QSplitter):
    """ Container widget to hold a QTabWidget which are separated by other 
    QTabWidgets via splitters.  
    
    An EditorAreaWidget is essentially a Node object in the editor area layout 
    tree.
    """

    def __init__(self, editor_area, parent=None, tabwidget=None):
        """ Creates an EditorAreaWidget object.

        editor_area : global AdvancedEditorAreaPane instance
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
        any of its descendents.
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
        editor_area : global AdvancedEditorAreaPane instance
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
        self.setUsesScrollButtons(True)
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
        empty_widget = self.create_empty_widget()
        self.addTab(empty_widget, 'dummy label')
        self.empty_widget = empty_widget
        self.tabBar().hide()
        self.setFocus()

    def hide_empty_widget(self):
        """ Hides the empty widget (containing buttons to open new file, and 
        collapse the split) based on whether the tabwidget is empty or not.
        """
        self.tabBar().show()
        index = self.indexOf(self.empty_widget)
        self.removeTab(index)
        self.empty_widget = None

    def create_empty_widget(self):
        """ Creates the QFrame object to be shown when the current tabwidget is 
        empty.
        """
        frame = QtGui.QFrame(parent=self)
        frame.setFrameShape(QtGui.QFrame.StyledPanel)
        layout = QtGui.QVBoxLayout(frame)
        layout.addStretch()

        # generate open button
        open_btn = QtGui.QPushButton('Open file', parent=frame)
        open_dlg = FileDialog(action='open')
        def _open():
            open_dlg.open()
            self.editor_area.active_tabwidget = self
            if open_dlg.return_code == OK:
                self.editor_area.task.open_file(open_dlg.path)
        open_btn.clicked.connect(_open)
        layout.addWidget(open_btn, alignment=QtCore.Qt.AlignHCenter)

        # generate collapse button
        if not self.parent().is_root():
            collapse_btn = QtGui.QPushButton('Close this pane', parent=frame)
            collapse_btn.clicked.connect(self.parent().collapse)
            layout.addWidget(collapse_btn, alignment=QtCore.Qt.AlignHCenter)

        # generate label
        label = QtGui.QLabel('Or, drop files here', 
                            parent=frame)
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
        editor_widget = self.widget(index)
        editor = self.editor_area._get_editor(editor_widget)
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
        global_pos = self.mapToGlobal(event.pos())
        menu = self.editor_area.get_context_menu(pos=global_pos)
        qmenu = menu.create_menu(self)
        qmenu.exec_(global_pos)

    def dragEnterEvent(self, event):
        """ Re-implemented to handle drag enter events 
        """
        accepted = False

        # handle tab drop events
        if self.editor_area._drag_info.enabled:
            accepted = True

        # handle file drop events from outside the application
        if event.mimeData().hasUrls():
            accepted = True

        # handle file drop events from the file browser pane
        if isinstance(event.mimeData(), PyMimeData):
            if getattr(event.mimeData().instance(), 'has_urls', False):
                accepted = True

        if accepted:
            self.editor_area.active_tabwidget = self
            self.setBackgroundRole(QtGui.QPalette.Highlight)
            event.acceptProposedAction()

        return super(DraggableTabWidget, self).dropEvent(event)

    def dropEvent(self, event):
        """ Re-implemented to handle drop events
        """
        accepted = False

        # handle tab drop events
        if self.editor_area._drag_info.enabled:
            # extract drag info
            from_index = self.editor_area._drag_info.from_index 
            widget = self.editor_area._drag_info.drag_widget
            from_tabwidget = self.editor_area._drag_info.from_tabwidget

            # extract drag widget label
            editor = self.editor_area._get_editor(widget)
            label = self.editor_area._get_label(editor)

            # if drop occurs at a tab bar, insert the tab at that position
            if not self.tabBar().tabAt(event.pos())==-1:
                index = self.tabBar().tabAt(event.pos())
                self.insertTab(index, widget, label)

            else:
                # if the drag initiated from the same tabwidget, put the tab 
                # back at the original index
                if self is from_tabwidget:
                    self.insertTab(from_index, widget, label)
                # else, just add it at the end
                else:
                    self.addTab(widget, label)
            
            # make the dropped widget active
            self.setCurrentWidget(widget)

            accepted = True

        # handle file drop events from outside the application
        if event.mimeData().hasUrls():
            # Build list of accepted files.
            extensions = tuple(self.editor_area.file_drop_extensions)
            file_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(extensions):
                    file_paths.append(file_path)
                elif self.editor_area.can_handle(file_path):
                    file_paths.append(file_path)

            # dispatch file drop event
            for file_path in file_paths:
                self.editor_area.active_tabwidget = self
                self.editor_area.file_dropped = file_path
                accepted = True

        # handle file drop events from the file browser pane
        if isinstance(event.mimeData(), PyMimeData):
            # Build list of accepted files.
            extensions = tuple(self.editor_area.file_drop_extensions)
            file_paths = []
            for url in event.mimeData().instance().urls:
                file_path = event.mimeData().instance().to_local_path(url)
                if file_path.endswith(extensions):
                    file_paths.append(file_path)
                elif self.editor_area.can_handle(file_path):
                    file_paths.append(file_path)

            # dispatch file drop event
            for file_path in file_paths:
                self.editor_area.active_tabwidget = self
                self.editor_area.file_dropped = file_path
                accepted = True

        if accepted:
            # empty out drag info, making the drag inactive again
            self.editor_area._drag_info.enabled = False
            event.acceptProposedAction()

        self.setBackgroundRole(QtGui.QPalette.Window)

    def dragLeaveEvent(self, event):
        """ Clear widget highlight on leaving
        """
        self.setBackgroundRole(QtGui.QPalette.Window)



class DraggableTabBar(QtGui.QTabBar):
    """ Implements a QTabBar with event filters for tab drag
    """
    def __init__(self, editor_area, parent):
        super(DraggableTabBar, self).__init__(parent)
        self.editor_area = editor_area
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

    def contextMenuEvent(self, event):
        """ Re-implemented to provide split/collapse context menu on the tab bar. 
        """
        global_pos = self.mapToGlobal(event.pos())
        menu = self.editor_area.get_context_menu(pos=global_pos)
        qmenu = menu.create_menu(self)
        qmenu.exec_(global_pos)

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.editor_area._drag_info.start_pos = event.pos()
            self.editor_area._drag_info.from_index = from_index \
                                                   = self.tabAt(event.pos())
            self.editor_area._drag_info.drag_widget = \
                                            self.parent().widget(from_index)
            self.editor_area._drag_info.from_tabwidget = self.parent()
        return super(DraggableTabBar, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # is the left mouse button still pressed?
        if not event.buttons()==QtCore.Qt.LeftButton:
            pass
        # has the mouse been dragged for sufficient distance?
        elif ((event.pos() - self.editor_area._drag_info.start_pos).manhattanLength()
            < QtGui.QApplication.startDragDistance()):
            pass
        # initiate drag
        else:
            self.editor_area._drag_info.enabled = True
            self.editor_area._drag_info.pixmap = self.editor_area._get_dragpixmap()
            drag = QtGui.QDrag(self.editor_area._drag_info.widget)
            mimedata = QtCore.QMimeData()
            drag.setPixmap(self.editor_area._drag_info.pixmap)
            drag.setMimeData(mimedata)
            drag.exec_()
            return
        return super(DraggableTabBar, self).mouseMoveEvent(event)

