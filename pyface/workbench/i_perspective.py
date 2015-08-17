""" The perspective interface. """


# Enthought library imports.
from traits.api import Bool, Interface, List, Str, Tuple

# Local imports.
from .perspective_item import PerspectiveItem


class IPerspective(Interface):
    """ The perspective interface. """

    # The perspective's unique identifier (unique within a workbench window).
    id = Str

    # The perspective's name.
    name = Str

    # The contents of the perspective.
    contents = List(PerspectiveItem)

    # The size of the editor area in this perspective. A value of (-1, -1)
    # indicates that the workbench window should choose an appropriate size
    # based on the sizes of the views in the perspective.
    editor_area_size = Tuple

    # Is the perspective enabled?
    enabled = Bool

    # Should the editor area be shown in this perspective?
    show_editor_area = Bool

    #### Methods ##############################################################

    def create(self, window):
        """ Create the perspective in a workbench window. """

    def show(self, window):
        """ Called when the perspective is shown in a workbench window. """

#### EOF ######################################################################
