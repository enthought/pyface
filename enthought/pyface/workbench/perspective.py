""" The default perspective. """


# Enthought library imports.
from enthought.traits.api import Bool, HasTraits, List, Str, Tuple, implements

# Local imports.
from i_perspective import IPerspective
from perspective_item import PerspectiveItem


class Perspective(HasTraits):
    """ The default perspective. """

    implements(IPerspective)
    
    # The ID of the default perspective.
    DEFAULT_ID = 'enthought.pyface.workbench.default'

    # The name of the default perspective.
    DEFAULT_NAME = 'Default'
    
    #### 'IPerspective' interface #############################################

    # The perspective's unique identifier (unique within a workbench window).
    id = Str(DEFAULT_ID)

    # The perspective's name.
    name = Str(DEFAULT_NAME)

    # The contents of the perspective.
    contents = List(PerspectiveItem)

    # The size of the editor area in this perspective. A value of (-1, -1)
    # indicates that the workbench window should choose an appropriate size
    # based on the sizes of the views in the perspective.
    editor_area_size = Tuple((-1, -1))

    # Is the perspective enabled?
    enabled = Bool(True)

    # Should the editor area be shown in this perspective?
    show_editor_area = Bool(True)
    
    ###########################################################################
    # 'Perspective' interface.
    ###########################################################################

    #### Initializers #########################################################

    def _id_default(self):
        """ Trait initializer. """

        # If no Id is specified then use the name.
        return self.name

    #### Methods ##############################################################
    
    def create(self, window):
        """ Create the perspective in a workbench window.

        For most cases you should just be able to set the 'contents' trait to
        lay out view as required. However, you can override this method if
        you want to have complete control over how the perspective is created.
        
        """

        # Set the size of the editor area.
        if self.editor_area_size != (-1, -1):
            window.editor_area_size = self.editor_area_size

        # If the perspective has specific contents then add just those.
        if len(self.contents) > 0:
            self._add_contents(window, self.contents)

        # Otherwise, add all of the views defined in the window at their
        # default positions realtive to the editor area.
        else:
            self._add_all(window)

        # Activate the first view in every region.
        window.reset_views()
        
        return
    
    ###########################################################################
    # Private interface.
    ###########################################################################

    def _add_contents(self, window, contents):
        """ Adds the specified contents. """

        # If we are adding specific contents then we ignore any default view
        # visibility.
        #
        # fixme: This is a bit ugly! Why don't we pass the visibility in to
        # 'window.add_view'?
        for view in window.views:
            view.visible = False
        
        for item in contents:
            self._add_perspective_item(window, item)
            
        return

    def _add_perspective_item(self, window, item):
        """ Adds a perspective item to a window. """

        # If no 'relative_to' is specified then the view is positioned
        # relative to the editor area.
        if len(item.relative_to) > 0:
            relative_to = window.get_view_by_id(item.relative_to)
            
        else:
            relative_to = None

        # fixme: This seems a bit ugly, having to reach back up to the
        # window to get the view. Maybe its not that bad?
        view = window.get_view_by_id(item.id)

        # Add the view to the window.
        window.add_view(
            view, item.position, relative_to, (item.width, item.height)
        )

        return
    
    def _add_all(self, window):
        """ Adds *all* of the window's views defined in the window. """

        for view in window.views:
            if view.visible:
                self._add_view(window, view)

        return

    def _add_view(self, window, view):
        """ Adds a view to a window. """

        # If no 'relative_to' is specified then the view is positioned
        # relative to the editor area.
        if len(view.relative_to) > 0:
            relative_to = window.get_view_by_id(view.relative_to)
            
        else:
            relative_to = None

        # Add the view to the window.
        window.add_view(
            view, view.position, relative_to, (view.width, view.height)
        )

        return

#### EOF ######################################################################
