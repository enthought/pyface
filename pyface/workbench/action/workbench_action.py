# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Abstract base class for all workbench actions. """


from pyface.workbench.api import WorkbenchWindow
from pyface.action.api import Action
from traits.api import Instance


class WorkbenchAction(Action):
    """ Abstract base class for all workbench actions. """

    # 'WorkbenchAction' interface -----------------------------------------#

    # The workbench window that the action is in.
    #
    # This is set by the framework.
    window = Instance(WorkbenchWindow)
