# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" A memento for a workbench window. """


from traits.api import Any, Dict, HasTraits, Str, Tuple


class WorkbenchWindowMemento(HasTraits):
    """ A memento for a workbench window. """

    # The Id of the active perspective.
    active_perspective_id = Str()

    # The memento for the editor area.
    editor_area_memento = Any()

    # Mementos for each perspective that has been seen.
    #
    # The keys are the perspective Ids, the values are the toolkit-specific
    # mementos.
    perspective_mementos = Dict(Str, Any)

    # The position of the window.
    position = Tuple()

    # The size of the window.
    size = Tuple()

    # Any extra data the toolkit implementation may want to keep.
    toolkit_data = Any()
