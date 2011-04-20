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
""" The event fired by the tree models/node monitors etc. """


# Enthought library imports.
from traits.api import Any, HasTraits, Int, List


# Classes for event traits.
class NodeEvent(HasTraits):
    """ The event fired by the tree models/node monitors etc. """

    # The node that has changed.
    node = Any

    # The nodes (if any) that have been inserted/removed/changed.
    children = List

    # The nodes (if any) that have been replaced.
    old_children = List

    # The starting index for nodes that have been inserted.
    index = Int

#### EOF ######################################################################
