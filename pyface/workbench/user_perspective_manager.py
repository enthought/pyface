# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Manages a set of user perspectives. """


import logging
import os


from pyface.workbench.api import Perspective
from traits.api import Any, Dict, HasTraits, Int, List, Property
from traits.api import Str


# Logging.
logger = logging.getLogger(__name__)


class UserPerspectiveManager(HasTraits):
    """ Manages a set of user perspectives. """

    # 'UserPerspective' interface -----------------------------------------#

    # A directory on the local file system that we can read and write to at
    # will. This is used to persist window layout information, etc.
    state_location = Str()

    # Next available user perspective id.
    next_id = Property(Int)

    # Dictionary mapping perspective id to user defined perspective definition.
    id_to_perspective = Property(Dict)

    # The list of user defined perspective definitions.
    perspectives = Property(List)

    # The name of the user defined perspectives definition file.
    file_name = Property(Str)

    # Private interface ----------------------------------------------------

    # Shadow trait for the 'id_to_perspective' property.
    _id_to_perspective = Any()

    # ------------------------------------------------------------------------
    # 'UserPerspective' interface.
    # ------------------------------------------------------------------------

    # Properties -----------------------------------------------------------

    def _get_next_id(self):
        """ Property getter. """

        # Get all of the current perspective ids:
        ids = list(self.id_to_perspective.keys())

        # If there are none:
        if len(ids) == 0:
            # Return the starting id:
            return 1

        # Else return the current highest id + 1 as the next id:
        ids.sort()

        return int(ids[-1][19:-2]) + 1

    def _get_id_to_perspective(self):
        """ Property getter. """

        if self._id_to_perspective is None:
            self._id_to_perspective = dic = {}
            try:
                fh = open(self.file_name, "r")
                for line in fh:
                    data = line.split(":", 1)
                    if len(data) == 2:
                        id, name = data[0].strip(), data[1].strip()
                        dic[id] = Perspective(
                            id=id, name=name, show_editor_area=False
                        )
                fh.close()
            except:
                pass

        return self._id_to_perspective

    def _get_perspectives(self):
        """ Property getter. """

        return list(self.id_to_perspective.values())

    def _get_file_name(self):
        """ Property getter. """

        return os.path.join(self.state_location, "__user_perspective__")

    # Methods -------------------------------------------------------------#

    def create_perspective(self, name, show_editor_area=True):
        """ Create a new (and empty) user-defined perspective. """

        perspective = Perspective(
            id="__user_perspective_%09d__" % self.next_id,
            name=name,
            show_editor_area=show_editor_area,
        )

        # Add the perspective to the map.
        self.id_to_perspective[perspective.id] = perspective

        # Update the persistent file information.
        self._update_persistent_data()

        return perspective

    def clone_perspective(self, window, perspective, **traits):
        """ Clone a perspective as a user perspective. """

        clone = perspective.clone_traits()

        # Give the clone a special user perspective Id!
        clone.id = "__user_perspective_%09d__" % self.next_id

        # Set any traits specified as keyword arguments.
        clone.trait_set(**traits)

        # Add the perspective to the map.
        self.id_to_perspective[clone.id] = clone

        # fixme: This needs to be pushed into the window API!!!!!!!
        window._memento.perspective_mementos[clone.id] = (
            window.layout.get_view_memento(),
            window.active_view and window.active_view.id or None,
            window.layout.is_editor_area_visible(),
        )

        # Update the persistent file information.
        self._update_persistent_data()

        return clone

    def save(self):
        """ Persist the current state of the user perspectives. """

        self._update_persistent_data()

    def add(self, perspective, name=None):
        """ Add a perspective with an optional name. """

        # Define the id for the new perspective:
        perspective.id = id = "__user_perspective_%09d__" % self.next_id

        # Save the new name (if specified):
        if name is not None:
            perspective.name = name

        # Create the perspective:
        self.id_to_perspective[id] = perspective

        # Update the persistent file information:
        self._update_persistent_data()

        # Return the new perspective created:
        return perspective

    def rename(self, perspective, name):
        """ Rename the user perspective with the specified id. """

        perspective.name = name

        self.id_to_perspective[perspective.id].name = name

        # Update the persistent file information:
        self._update_persistent_data()

    def remove(self, id):
        """ Remove the user perspective with the specified id.

        This method also updates the persistent data.

        """

        if id in self.id_to_perspective:
            del self.id_to_perspective[id]

            # Update the persistent file information:
            self._update_persistent_data()

            # Try to delete the associated perspective layout file:
            try:
                os.remove(os.path.join(self.state_location, id))
            except:
                pass

        return

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    def _update_persistent_data(self):
        """ Update the persistent file information. """

        try:
            fh = open(self.file_name, "w")
            fh.write(
                "\n".join(
                    ["%s: %s" % (p.id, p.name) for p in self.perspectives]
                )
            )
            fh.close()

        except:
            logger.error(
                "Could not write the user defined perspective "
                "definition file: " + self.file_name
            )

        return
