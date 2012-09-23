# Standard library imports.
import sys

# Enthought library imports.
from pyface.tasks.i_editor_area_pane import IEditorAreaPane, \
    MEditorAreaPane
from traits.api import implements, on_trait_change, Instance, List

# System library imports.
from pyface.qt import QtCore, QtGui
from pyface.action.api import Action, Group
from pyface.tasks.editor import Editor
from traitsui.api import Menu

# Local imports.
from task_pane import TaskPane
from util import set_focus
from canopy.ui.widget_events import ContextMenuEvent, set_context_menu_emit
from encore.events.api import BaseEventManager

###############################################################################
# 'SplitEditorAreaPane' class.
###############################################################################

class EditorAreaPane(TaskPane, MEditorAreaPane):
    """ The toolkit-specific implementation of a EditorAreaPane.

    See the IEditorAreaPane interface for API documentation.
    """

    implements(IEditorAreaPane)

    #### EditorAreaPane interface #############################################

    # Currently active tabwidget
    active_tabwidget = Instance(QtGui.QTabWidget)

    # List of tabwidgets
    tabwidgets = List(Instance(QtGui.QTabWidget))

    # tree based layout object 
    #layout = Instance(EditorAreaLayout) 

    ###########################################################################
    # 'TaskPane' interface.
    ###########################################################################

    def create(self, parent):
        """ Create and set the toolkit-specific control that represents the
            pane.
        """
        # Create and configure the Editor Area Widget.
        self.control = EditorAreaWidget(self, parent)
        self.drag_info = {}

        # handle application level focus changes
        QtGui.QApplication.instance().focusChanged.connect(self._focus_changed)

        em = self.task.window.application.get_service(BaseEventManager)
        em.connect(ContextMenuEvent, self.on_context_menu)

    def destroy(self):
        """ Destroy the toolkit-specific control that represents the pane.
        """        
        for editor in self.editors:
            self.remove_editor(editor)

        super(EditorAreaPane, self).destroy()

    ###########################################################################
    # 'IEditorAreaPane' interface.
    ###########################################################################

    def activate_editor(self, editor):
        """ Activates the specified editor in the pane.
        """
        self.active_editor = editor
        editor.control.setFocus()
        self.active_tabwidget = editor.control.parent().parent()
        self.active_tabwidget.setCurrentWidget(editor.control)
        
    def add_editor(self, editor):
        """ Adds an editor to the active_tabwidget
        """
        editor.editor_area = self
        editor.create(self.active_tabwidget)
        index = self.active_tabwidget.addTab(editor.control, self._get_label(editor))
        self.active_tabwidget.setTabToolTip(index, editor.tooltip)
        self.editors.append(editor)

    def remove_editor(self, editor):
        """ Removes an editor from the associated tabwidget
        """
        self.editors.remove(editor)
        tabwidget = editor.control.parent().parent()
        assert isinstance(tabwidget, QtGui.QTabWidget)
        tabwidget.removeTab(tabwidget.indexOf(editor.control))
        editor.destroy()
        editor.editor_area = None
        if not self.editors:
            self.active_editor = None


    ##########################################################################
    # 'EditorAreaPane' interface.
    ##########################################################################

    def get_layout(self):
        """ Returns a LayoutItem that reflects the current state of the 
        tabwidgets in the split framework.
        """
        #node = dict(left=a,right=b,data=dict(orientation, isChildless=True))
        pass

    def set_layout(self, layout):
        """ Applies a LayoutItem to the tabwidgets in the pane.
        """
        pass

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_label(self, editor):
        """ Return a tab label for an editor.
        """
        label = editor.name
        if editor.dirty:
            label = '*' + label
        return label

    def _get_editor(self, editor_widget):
        """ Returns the editor corresponding to editor_widget
        """
        for editor in self.editors:
            if editor.control is editor_widget:
                return editor
        return None

    def _next_tab(self):
        """ Activate the tab after the currently active tab.
        """
        index = self.active_tabwidget.currentIndex()
        index = index + 1 if index < active_tabwidget.count() - 1 else index
        self.active_tabwidget.setCurrentIndex(index)

    def _previous_tab(self):
        """ Activate the tab before the currently active tab.
        """
        index = self.active_tabwidget.currentIndex()
        index = index - 1 if index > 0  else index
        self.active_tabwidget.setCurrentIndex(index)

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
            for editor in self.editors:
                control = editor.control
                if control is not None and control.isAncestorOf(new):
                    self.activate_editor(editor)
            if isinstance(new, DraggableTabWidget):
                self.active_tabwidget = new
            elif isinstance(new, QtGui.QTabBar):
                self.active_tabwidget = new.parent() 

    def on_context_menu(self, event):
        """ Adds split/collapse context menu actions
        """
        if isinstance(event.source, QtGui.QTabWidget):
            tabwidget = event.source
        else:
            tabwidget = event.source.control.parent().parent()
        splitter = tabwidget.parent()

        # add this group only if it has not been added before
        if not event.menu.find_group(id='split'):
            # add split actions (only show for non-empty tabwidgets)
            if not splitter.is_empty():
                actions = [Action(id='split_hor', name='Split horizontally', 
                           on_perform=lambda : splitter.split(orientation=
                            QtCore.Qt.Horizontal)),
                           Action(id='split_ver', name='Split vertically', 
                           on_perform=lambda : splitter.split(orientation=
                            QtCore.Qt.Vertical))]

                splitgroup = Group(*actions, id='split')
                event.menu.append(splitgroup)

        # add this group only if it has not been added before
        if not event.menu.find_group(id='collapse'):
            # add collapse action (only show for collapsible splitters)
            if splitter.is_collapsible():
                actions = [Action(id='merge', name='Collapse split', 
                            on_perform=lambda : splitter.collapse())]

                collapsegroup = Group(*actions, id='collapse')
                event.menu.append(collapsegroup)


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

        editor_area : global EditorAreaPane instance
        parent : parent splitter
        tabwidget : tabwidget object contained by this splitter

        """
        super(EditorAreaWidget, self).__init__(parent=parent)
        self.editor_area = editor_area
        
        if not tabwidget:
            tabwidget = DraggableTabWidget(editor_area=self.editor_area, parent=self)

        # add the tabwidget to the splitter
        self.addWidget(tabwidget)
        
        # Initializes left and right children to None (since no initial splitter
        # children are present) 
        self.leftchild = None 
        self.rightchild = None

    def tabwidget(self):
        """ Obtain the tabwidget associated with current EditorAreaWidget
        """
        for child in self.children():
            if isinstance(child, QtGui.QTabWidget):
                return child
        return None

    def brother(self):
        """ Returns another child of its parent. Returns None if it can't find any 
        brother.
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
        """ Returns True if the current EditorAreaWidget is a leaf, i.e., it has a 
        tabwidget as one of it's immediate child.
        """
        # a leaf has it's leftchild and rightchild None
        if not self.leftchild and not self.rightchild:
            return True
        return False

    def is_empty(self):
        """ Returns True if the current splitter's tabwidget doesn't contain any 
        tab.
        """
        return not bool(self.tabwidget().count())

    def is_collapsible(self):
        """ Returns True if the current splitter can be collapsed to its brother, i.e.
        if it is a) either empty, or b) it has a brother which is a leaf.
        """
        if self.is_root():
            return False
        
        if self.is_empty():
            return True
        
        parent = self.parent()
        brother = self.brother()
            
        if brother.is_leaf():
            return True
        else:
            return False

    def split(self, orientation=QtCore.Qt.Horizontal):
        """ Split the current splitter into two children splitters. The tabwidget is 
        moved to the left child while a new empty tabwidget is added to the right 
        child.
        
        orientation : whether to split horizontally or vertically
        """
        # set splitter orientation
        self.setOrientation(orientation)
        orig_size = self.sizes()[0]

        # create new children
        self.leftchild = EditorAreaWidget(self.editor_area, tabwidget=self.tabwidget())
        self.rightchild = EditorAreaWidget(self.editor_area, tabwidget=None)

        # add newly generated children
        self.addWidget(self.leftchild)
        self.addWidget(self.rightchild)

        # set equal sizes of splits
        self.setSizes([orig_size/2,orig_size/2])
        
        # make the rightchild's tabwidget active
        self.editor_area.active_tabwidget = self.rightchild.tabwidget()

    def collapse(self):
        """ Collapses the current splitter and its brother splitter to their 
        parent splitter. Merges together the tabs of both's tabwidgets. 

        Does nothing if the current splitter is not collapsible.
        """
        if not self.is_collapsible():
            return

        # save original currentwidget to make active later
        orig_currentWidget = self.tabwidget().currentWidget()

        parent = self.parent()
        brother = self.brother()

        left = parent.leftchild.tabwidget()
        right = parent.rightchild.tabwidget()
        target = DraggableTabWidget(editor_area=self.editor_area, parent=parent)

        # add tabs of left and right tabwidgets to target
        for source in (left, right):
            # Note: addTab removes widgets from source tabwidget, so 
            # grabbing all the source widgets beforehand
            widgets = [source.widget(i) for i in range(source.count())]
            for editor_widget in widgets:
                editor = self.editor_area._get_editor(editor_widget)
                target.addTab(editor_widget, 
                            self.editor_area._get_label(editor))                    

        # add target to parent
        parent.addWidget(target)

        # activate the active widget of source tabwidget
        target.setCurrentWidget(orig_currentWidget)

        # remove parent's splitter children
        self.deleteLater()
        brother.deleteLater()
        parent.leftchild = None
        parent.rightchild = None
    

class DraggableTabWidget(QtGui.QTabWidget):
    """ Implements a QTabWidget with event filters for tab drag and drop
    """

    def __init__(self, editor_area, parent):
        """ 
        editor_area : EditorAreaPane instance
        parent : parent of the tabwidget
        """
        super(DraggableTabWidget, self).__init__(parent)
        self.editor_area = editor_area

        # configure QTabWidget
        self.setTabBar(DraggableTabBar(editor_area=editor_area, parent=self))
        self.setDocumentMode(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusProxy(None)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)

        # set drop and context menu policies
        self.setAcceptDrops(True)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        # connecting signals
        self.currentChanged.connect(self._update_active_editor)
        self.tabCloseRequested.connect(self._close_requested)
        #self._filter = TabWidgetFilter(self.editor_area)
        #self.tab_bar = self.tabBar()
        #self.tab_bar.installEventFilter(self._filter)

    def get_names(self):
        """ Utility function to return names of all the editors open in the 
        current tabwidget.
        """
        names = []
        for i in range(self.count()):
            editor_widget = self.widget(i)
            editor = self.editor_area._get_editor(editor_widget)
            names.append(editor.name)
        return names


    ###### Signal handlers #####################################################

    def _close_requested(self, index):
        """ Re-implemented to close the editor when it's tab is closed
        """
        editor_widget = self.widget(index)
        editor = self.editor_area._get_editor(editor_widget)
        editor.close()

        if self.count()==0:
            self.parent().collapse()


    def _update_active_editor(self, index):
        """ Updates editor area's active editor when current index changes
        """
        editor_widget = self.widget(index)
        editor = self.editor_area._get_editor(editor_widget)
        self.editor_area.active_editor = editor

    ##### Event handlers #######################################################

    def contextMenuEvent(self, event):
        """ To fire ContextMenuEvent even on empty tabwidgets
        """
        parent = self.parent()
        if parent.is_empty():
            menu = Menu()
            em = (self.editor_area.task.window.application.
                    get_service(BaseEventManager))
            evt = ContextMenuEvent(source=self, widget=parent, 
                                pos=event.pos(), menu=menu)
            em.emit(evt)
            qmenu = menu.create_menu(self)
            qmenu.show()
        return super(DraggableTabWidget, self).contextMenuEvent(event)            

    def dragEnterEvent(self, event):
        """ Re-implemented to handle drag enter events 
        """
        if self.editor_area.drag_info:
            event.acceptProposedAction()

        return super(DraggableTabWidget, self).dropEvent(event)

    def dropEvent(self, event):
        """ Re-implemented to handle drop events
        """
        if self.editor_area.drag_info:
            from_index = self.editor_area.drag_info['from_index'] 
            widget = self.editor_area.drag_info['widget']
            from_tabwidget = self.editor_area.drag_info['from_tabwidget']

            editor = self.editor_area._get_editor(widget)
            label = self.editor_area._get_label(editor)
            if self is from_tabwidget:
                self.insertTab(from_index, widget, label)
            else:
                if not self.tabBar().tabAt(event.pos())==-1:
                    index = self.tabBar().tabAt(event.pos())
                    self.insertTab(index, widget, label)
                else:
                    self.addTab(widget, label)
                from_tabwidget.removeTab(from_index)
            self.setCurrentWidget(widget)
            self.editor_area.drag_info = {}
            event.acceptProposedAction()
        #return super(DraggableTabWidget, self).dropEvent(event)


class DraggableTabBar(QtGui.QTabBar):
    """ Implements a QTabBar with event filters for tab drag and drop
    """
    def __init__(self, editor_area, parent):
        super(DraggableTabBar, self).__init__(parent)
        self.editor_area = editor_area
        #self.setAcceptDrops(True)

    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.LeftButton:
            self.editor_area.drag_info['from_index'] = from_index = self.tabAt(event.pos())
            self.editor_area.drag_info['widget'] = widget = self.parent().widget(from_index)
            self.editor_area.drag_info['from_tabwidget'] = self.parent()
            self.editor_area.drag_info['pixmap'] = QtGui.QPixmap.grabWidget(widget)
        return super(DraggableTabBar, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        # is the left mouse button still pressed?
        if not event.buttons()==QtCore.Qt.LeftButton:
            pass
        # is the pointer still within tab bar area?
        if self.rect().contains(event.pos()):
            pass
        # initiate drag
        else:
            drag = QtGui.QDrag(self.editor_area.drag_info['widget'])
            mimedata = QtCore.QMimeData()
            drag.setPixmap(self.editor_area.drag_info['pixmap'])
            drag.setMimeData(mimedata)
            drag.exec_()
        return super(DraggableTabBar, self).mouseMoveEvent(event)


class TabWidgetFilter(QtCore.QObject):
    """ Handles tab widget focus and drag/drop events
    """
    def __init__(self, editor_area):
        super(TabWidgetFilter, self).__init__()
        self.editor_area = editor_area

    def eventFilter(self, object, event):
        """ Handle drag and drop events with MIME type 'text/uri-list'.
        """
        if event.type() in (QtCore.QEvent.DragEnter, QtCore.QEvent.Drop):
            # Build list of accepted files.
            extensions = tuple(self.editor_area.file_drop_extensions)
            file_paths = []
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(extensions):
                    file_paths.append(file_path)

            # Accept the event if we have at least one accepted file.
            if event.type() == QtCore.QEvent.DragEnter:
                if file_paths:
                    event.acceptProposedAction()

            # Dispatch the events.
            elif event.type() == QtCore.QEvent.Drop:
                for file_path in file_paths:
                    self.editor_area.file_dropped = file_path

            return True

        # Handle drag/drop events on QTabBar
        if isinstance(object, QtGui.QTabBar):
            # register drag widget
            if event.type() == QtCore.QEvent.MouseButtonPress:
                from_index = object.tabAt(event.pos())
                self.editor_area.drag_widget = object.parent().widget(from_index)
                
            # initiate drag event
            if event.type() == QtCore.QEvent.MouseMove:
                # if mouse isn't dragged outside of tab bar then return
                if object.rect().contains(event.pos()):
                    return False
                # initiate drag, send a drop event
                else:
                    drag = QtGui.QDrag(self.editor_area.drag_widget)
                    drag_widget = self.editor_area.drag_widget
                    tabwidget = object.parent()
                    tabIcon = tabwidget.tabIcon(tabwidget.indexOf(drag_widget))
                    iconPixmap = tabIcon.pixmap(QtCore.QSize(22,22))
                    iconPixmap = QtGui.QPixmap.grabWidget(drag_widget)
                    mimeData = QtCore.QMimeData()
                    drag.setPixmap(iconPixmap)
                    drag.setMimeData(mimeData)
                    dropAction = drag.exec_()
                    return True

        return False