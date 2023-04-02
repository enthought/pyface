# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The event fired by the tree models/node monitors etc. """


from traits.api import Any, HasTraits, Int, List


# Classes for event traits.
class NodeEvent(HasTraits):
    """ The event fired by the tree models/node monitors etc. """

    # The node that has changed.
    node = Any()

    # The nodes (if any) that have been inserted/removed/changed.
    children = List()

    # The nodes (if any) that have been replaced.
    old_children = List()

    # The starting index for nodes that have been inserted.
    index = Int()
