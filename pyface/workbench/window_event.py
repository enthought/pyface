""" Window events. """


# Enthought library imports.
from traits.api import HasTraits, Instance, Vetoable

# Local imports.
from .workbench_window import WorkbenchWindow


class WindowEvent(HasTraits):
    """ A window lifecycle event. """

    #### 'WindowEvent' interface ##############################################

    # The window that the event occurred on.
    window = Instance(WorkbenchWindow)


class VetoableWindowEvent(WindowEvent, Vetoable):
    """ A vetoable window lifecycle event. """

    pass

#### EOF ######################################################################
