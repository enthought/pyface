# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for all content viewers. """


from traits.api import Any, Instance, List


from .viewer import Viewer
from .viewer_filter import ViewerFilter
from .viewer_sorter import ViewerSorter


class ContentViewer(Viewer):
    """ Abstract base class for all content viewers.

    A content viewer is a model-based adapter on some underlying
    toolkit-specific widget that acceses the model via a content provider and
    a label provider.

    The content provider provides the actual elements in the model.  The label
    provider provides a label for each element consisting of text and/or an
    image.

    """

    # The domain object that is the root of the viewer's data.
    input = Any()

    # The content provider provides the data elements for the viewer.
    #
    # Derived classes specialize this trait with the specific type of the
    # content provider that they require (e.g. the tree viewer MUST have a
    # 'TreeContentProvider').
    content_provider = Any()

    # The label provider provides labels for each element.
    #
    # Derived classes specialize this trait with the specific type of the label
    # provider that they require (e.g. the table viewer MUST have a
    # 'TableLabelProvider').
    label_provider = Any()

    # The viewer's sorter (None if no sorting is required).
    sorter = Instance(ViewerSorter)

    # The viewer's filters.
    filters = List(ViewerFilter)
