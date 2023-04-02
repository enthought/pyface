# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" An action that sets an attribute. """


from traits.api import Any, Str


from .workbench_action import WorkbenchAction


class SetattrAction(WorkbenchAction):
    """ An action that sets an attribute. """

    # 'SetattrAction' interface --------------------------------------------

    # The object that we set the attribute on.
    obj = Any()

    # The name of the attribute that we set.
    attribute_name = Str()

    # The value that we set the attribute to.
    value = Any()

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Performs the action. """

        setattr(self.obj, self.attribute_name, self.value)

        return
