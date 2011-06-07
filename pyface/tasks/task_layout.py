# Standard library imports.
from cStringIO import StringIO
import sys

# Enthought library imports.
from enthought.traits.api import Either, Enum, HasStrictTraits, Int, List, \
     Str, This


class LayoutItem(HasStrictTraits):
    """ The base class for all Task-related layout objects.
    """

    def __repr__(self):
        return self.pformat()

    def pargs(self):
        return []

    def pformat(self):
        """ Pretty-format the layout item. Returns a string.
        """
        stream = StringIO()
        self.pstream(stream)
        return stream.getvalue()

    def pprint(self):
        """ Pretty-prints the layout item.
        """
        self.pstream(sys.stdout)

    def pstream(self, stream, indent=0):
        """ Pretty-formats the layout item to a stream.
        """
        call = self.__class__.__name__ + '('
        indent += len(call)
        stream.write(call)

        args = [ (None, arg) for arg in self.pargs() ]
        traits = []
        for name, trait in sorted(self.traits().iteritems()):
            if not trait.pretty_skip and not trait.transient:
                value = getattr(self, name)
                if trait.default != value:
                    traits.append((name, value))
        traits.sort()
        args.extend(traits)

        for i, (name, value) in enumerate(args):
            if name:
                stream.write(name + '=')
            if isinstance(value, LayoutItem):
                value.pstream(stream, indent)
            else:
                stream.write(repr(value))
            if i < len(args) - 1:
                stream.write(',\n')
                stream.write(indent * ' ')
            
        stream.write(')')
    

class LayoutContainer(LayoutItem):
    """ The base class for all layout items that contain other layout items.
    """

    items = List(pretty_skip=True)

    def __init__(self, *items, **traits):
        super(LayoutContainer, self).__init__(**traits)
        self.items = list(items)

    def pargs(self):
        return self.items
    

class PaneItem(LayoutItem):
    """ A pane in a Task layout.
    """

    # The ID of the TaskPane to which the item refers.
    id = Str(pretty_skip=True)

    # The width of the pane in pixels. If not specified, the pane will be sized
    # according to its size hint.
    width = Int(-1)

    # The height of the pane in pixels. If not specified, the pane will be sized
    # according to its size hint.
    height = Int(-1)

    def __init__(self, id, **traits):
        super(Pane, self).__init__(**traits)
        self.id = id

    def pargs(self):
        return [ self.id ]


class Tabbed(LayoutContainer):
    """ A tab area in a Task layout.
    """

    # A tabbed layout can only contain PaneItems as sub-items. Splitters and
    # other Tabbed layouts are not allowed.
    items = List(PaneItem, pretty_skip=True)

    # The ID of the TaskPane which is active in layout. If not specified, the
    # first pane is active.
    active_tab = Str
    

class Splitter(LayoutContainer):
    """ A split area in a Task layout.
    """

    # The orientation of the splitter.
    orientation = Enum('horizontal', 'vertical')

    # The sub-items of the splitter, which are PaneItems, Tabbed layouts, and
    # other Splitters.
    items = List(Either(PaneItem, Tabbed, This), pretty_skip=True)
    
class HSplitter(Splitter):
    """ A convenience class for horizontal splitters.
    """
    orientation = Str('horizontal')

class VSplitter(Splitter):
    """ A convenience class for vertical splitters.
    """
    orientation = Str('vertical')


class DockArea(LayoutContainer):
    """ A dock area in a Task layout.
    """

    # The location of the dock area. Must be specified.
    area = Enum(None, ('left', 'right', 'top', 'bottom'))

    # The layout items in the dock area, which are PaneItems, Tabbed layouts,
    # and Splitters.
    items = List(Either(PaneItem, Tabbed, Splitter), pretty_skip=True)


class TaskLayout(LayoutContainer):
    """ The layout of a Task.
    """

    # The ID of the task for which this is a layout.
    id = Str

    # The dock area layouts for the task.
    items = List(DockArea, pretty_skip=True)

    # Assignments of dock areas to the window's corners. By default, the top and
    # bottom dock areas extend into both of the top and both of the bottom
    # corners, respectively.
    top_left_corner = Enum('top', 'left')
    top_right_corner = Enum('top', 'right')
    bottom_left_corner = Enum('bottom', 'left')
    bottom_right_corner = Enum('bottom', 'right')
