""" A memento for a workbench window. """


# Enthought library imports.
from traits.api import Any, Dict, HasTraits, Str, Tuple


class WorkbenchWindowMemento(HasTraits):
    """ A memento for a workbench window. """

    # The Id of the active perspective.
    active_perspective_id = Str

    # The memento for the editor area.
    editor_area_memento = Any

    # Mementos for each perspective that has been seen.
    #
    # The keys are the perspective Ids, the values are the toolkit-specific
    # mementos.
    perspective_mementos = Dict(Str, Any)

    # The position of the window.
    position = Tuple

    # The size of the window.
    size = Tuple

    # Any extra data the toolkit implementation may want to keep.
    toolkit_data = Any()


#### EOF ######################################################################
