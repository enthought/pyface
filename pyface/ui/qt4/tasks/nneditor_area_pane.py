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
        self.drag_widget = None

        # handle application level focus changes
        QtGui.QApplication.instance().focusChanged.connect(self._focus_changed)

        # handle context menu events
        event_manager = (self.task.window.application.get_service(BaseEventManager))
        event_manager.connect(ContextMenuEvent, self.context_menu_actions)

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
            self.active_tabwidget = None


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
        #print 'old: ', old, '\tnew: ', new
        if new:
            for editor in self.editors:
                control = editor.control
                if control is not None and control.isAncestorOf(new):
                    self.active_editor = editor#self.activate_editor(editor)
            if isinstance(new, DraggableTabWidget):
                self.active_tabwidget = new
            elif isinstance(new, QtGui.QTabBar):
                self.active_tabwidget = new.parent() 

    def context_menu_actions(self, event):
        """ Adds split/collapse context menu actions
        """
        if isinstance(event.source, QtGui.QTabWidget):
            tabwidget = event.source
        else:
            tabwidget = event.source.control.parent().parent()
        splitter = tabwidget.parent()

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

        # add collapse action (only show for non root splitters)
        if not splitter.is_root():
            actions = [Action(id='merge', name='Collapse split', 
                        on_perform=lambda : splitter.collapse())]

            collapsegroup = Group(*actions, id='collapse')
            event.menu.append(collapsegroup)

    def _add_split_actions(self, event):
        """ Adds "Split horizontally"/"Split vertically" action buttons to the 
        contextmenu
        """
        print 'src:'
        print event.source.name
        # add these actions only if they have not been added before
        if event.menu.find_group(id='split'):
            return

        if isinstance(event.source, QtGui.QTabWidget):
            tabwidget = event.source
        else:
            tabwidget = event.source.control.parent().parent()
        splitter = tabwidget.parent()
        
        actions = [Action(id='split_hor', name='Split horizontally', 
                  on_perform=lambda : splitter.split(orientation=QtCore.Qt.Horizontal)),
                   Action(id='split_ver', name='Split vertically', 
                  on_perform=lambda : splitter.split(orientation=QtCore.Qt.Vertical))]

        group = Group(*actions, id='split')
        event.menu.append(group)

    def _add_collapse_action(self, event):
        """ Adds "Collapse split" action button to the contextmenu
        """
        # show collapse action only when there is a brother to collapse with
        if not self.brother():
            return

        # add this action only if it has not been added before
        if event.menu.find_group(id='collapse'):
            return

        if isinstance(event.source, QtGui.QTabWidget):
            tabwidget = event.source
        else:
            tabwidget = event.source.control.parent().parent()
        splitter = tabwidget.parent()
        
        actions = [Action(id='merge', name='Collapse split', 
                  on_perform=lambda : splitter.collapse())]

        group = Group(*actions, id='collapse')
        event.menu.append(group)


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

        # dirty hack to check if self is root
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

    def is_empty(self):
        """ Returns True if the current tabwidget doesn't contain any editor.
        """
        return not bool(self.tabwidget().count())

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
        """
        parent = self.parent()
        brother = self.brother()

        left = parent.leftchild.tabwidget()
        right = parent.rightchild.tabwidget()
        target = DraggableTabWidget(editor_area=self.editor_area, parent=parent)

        # add tabs of left and right tabwidgets to target
        for source in (left, right):
            for i in range(source.count()):
                editor_widget = source.widget(i)
                editor = self.editor_area._get_editor(editor_widget)
                target.addTab(editor_widget, 
                            self.editor_area._get_label(editor))

        left.deleteLater()
        right.deleteLater()

        # add target to parent
        parent.addWidget(target)

        # activate the active widget of current tabwidget
        target.setCurrentWidget(self.tabwidget().currentWidget())

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
        self.setTabBar(QtGui.QTabBar(parent=self))
        self.setAcceptDrops(True)
        self.setDocumentMode(True)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setFocusProxy(None)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)

        # event handling
        self._filter = TabWidgetFilter(self.editor_area)
        self.tab_bar = self.tabBar()
        self.tab_bar.installEventFilter(self._filter)


    ###### Signal handlers #####################################################

    def tabRemoved(self, index):
        """ Re-implemented to collapse splitter when no tab is present
        """
        editor_widget = self.widget(index)

        # find the editor correspinding to this widget, and close it
        for editor in self.editor_area.editors:
            if editor.control==editor_widget:
                editor.close()
                break

        # collapse split if all tabs are closed
        if self.count()==0:
            self.parent().collapse()

    def mousePressEvent(self, event):
        """ Re-implemented to fire ContextMenuEvent even on empty tabwidgets
        """
        if event.button() == QtCore.Qt.RightButton and not self.count():
            event_manager = (self.editor_area.task.window.
                            application.get_service(BaseEventManager))
            parent = self.parent()
            if not parent.is_root():
                print 'mouse press event on tabwidget'
                set_context_menu_emit(target=self, widget=parent,
                            event_manager=event_manager, 
                            default_handler=self.editor_area.context_menu_actions)

    def dragEnterEvent(self, event):
        """ Re-implemented to handle drag enter events 
        """
        print 'drag enter'
        mimeData = event.mimeData()
        
        print mimeData
        #from IPython.core.debugger import Tracer; Tracer()()
        #if mimeData.hasFormat("text/plain"):
        event.acceptProposedAction()

    def dropEvent(self, event):
        """ Re-implemented to handle drop events
        """
        drag_widget = self.editor_area.drag_widget 
        self.addTab(drag_widget, self.editor_area._get_label(drag_widget))
        event.acceptProposedAction()


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