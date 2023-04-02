# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Window events. """


from traits.api import HasTraits, Instance, Vetoable


from .workbench_window import WorkbenchWindow


class WindowEvent(HasTraits):
    """ A window lifecycle event. """

    # 'WindowEvent' interface ---------------------------------------------#

    # The window that the event occurred on.
    window = Instance(WorkbenchWindow)


class VetoableWindowEvent(WindowEvent, Vetoable):
    """ A vetoable window lifecycle event. """

    pass
