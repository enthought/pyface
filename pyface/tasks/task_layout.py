# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from io import StringIO
import sys


from traits.api import (
    Enum, HasStrictTraits, Int, Instance, List, Str, Union,
)


class LayoutItem(HasStrictTraits):
    """ The base class for all Task-related layout objects.
    """

    def __repr__(self):
        return self.pformat()

    def iterleaves(self):
        yield self

    def pargs(self):
        return []

    def pformat(self, indent=0, multiline=False):
        """ Pretty-format the layout item. Returns a string.
        """
        stream = StringIO()
        self.pstream(stream, indent, multiline)
        return stream.getvalue()

    def pprint(self, indent=0, multiline=False):
        """ Pretty-prints the layout item.
        """
        self.pstream(sys.stdout, indent, multiline)

    def pstream(self, stream, indent=0, multiline=False):
        """ Pretty-formats the layout item to a stream.
        """
        call = self.__class__.__name__ + "("
        indent += len(call)
        stream.write(call)

        args = [(None, arg) for arg in self.pargs()]
        traits = []
        for name, trait in sorted(self.traits().items()):
            if not trait.pretty_skip and not trait.transient:
                value = getattr(self, name)
                if trait.default != value:
                    traits.append((name, value))
        traits.sort()
        args.extend(traits)

        for i, (name, value) in enumerate(args):
            arg_indent = indent
            if name:
                arg_indent += len(name) + 1
                stream.write(name + "=")
            if isinstance(value, LayoutItem):
                value.pstream(stream, arg_indent, multiline)
            else:
                stream.write(repr(value))
            if i < len(args) - 1:
                stream.write(",")
                if multiline:
                    stream.write("\n" + indent * " ")
                else:
                    stream.write(" ")

        stream.write(")")


class LayoutContainer(LayoutItem):
    """ The base class for all layout items that contain other layout items.
    """

    items = List(pretty_skip=True)

    def __init__(self, *items, **traits):
        # Items may either be specified as a positional arg or a kwarg.
        if items:
            if "items" in traits:
                raise ValueError(
                    "Received 'items' as positional and keyword argument."
                )
            else:
                traits["items"] = list(items)
        super().__init__(**traits)

    def iterleaves(self):
        for item in self.items:
            for leaf in item.iterleaves():
                yield leaf

    def pargs(self):
        return self.items


class PaneItem(LayoutItem):
    """ A pane in a Task layout.
    """

    #: The ID of the item. If the item refers to a TaskPane, this is the ID of
    #: that TaskPane.
    id = Union(Str, Int, default_value="", pretty_skip=True)

    #: The width of the pane in pixels. If not specified, the pane will be
    #: sized according to its size hint.
    width = Int(-1)

    #: The height of the pane in pixels. If not specified, the pane will be
    #: sized according to its size hint.
    height = Int(-1)

    def __init__(self, id="", **traits):
        super().__init__(**traits)
        self.id = id

    def pargs(self):
        return [self.id]


class Tabbed(LayoutContainer):
    """ A tab area in a Task layout.
    """

    #: A tabbed layout can only contain PaneItems as sub-items. Splitters and
    #: other Tabbed layouts are not allowed.
    items = List(PaneItem, pretty_skip=True)

    #: The ID of the TaskPane which is active in layout. If not specified, the
    #: first pane is active.
    active_tab = Union(Str, Int, default_value="")


class Splitter(LayoutContainer):
    """ A split area in a Task layout.
    """

    #: The orientation of the splitter.
    orientation = Enum("horizontal", "vertical")

    #: The sub-items of the splitter, which are PaneItems, Tabbed layouts, and
    #: other Splitters.
    items = List(
        Union(
            Instance(PaneItem),
            Instance(Tabbed),
            Instance("pyface.tasks.task_layout.Splitter"),
        ),
        pretty_skip=True,
    )


class HSplitter(Splitter):
    """ A convenience class for horizontal splitters.
    """

    orientation = Str("horizontal")


class VSplitter(Splitter):
    """ A convenience class for vertical splitters.
    """

    orientation = Str("vertical")


class DockLayout(LayoutItem):
    """ The layout for a main window's dock area.
    """

    # The layouts for the task's dock panes.
    left = Union(Instance(PaneItem), Instance(Tabbed), Instance(Splitter))
    right = Union(Instance(PaneItem), Instance(Tabbed), Instance(Splitter))
    top = Union(Instance(PaneItem), Instance(Tabbed), Instance(Splitter))
    bottom = Union(Instance(PaneItem), Instance(Tabbed), Instance(Splitter))

    #: Assignments of dock areas to the window's corners. By default, the top
    #: and bottom dock areas extend into both of the top and both of the
    #: bottom corners, respectively.
    top_left_corner = Enum("top", "left")
    top_right_corner = Enum("top", "right")
    bottom_left_corner = Enum("bottom", "left")
    bottom_right_corner = Enum("bottom", "right")


class TaskLayout(DockLayout):
    """ The layout for a Task.
    """

    #: The ID of the task for which this is a layout.
    id = Str()
