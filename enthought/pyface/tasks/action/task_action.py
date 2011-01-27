# Standard library imports.
import logging

# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.traits.api import Str

# Logging.
logger = logging.getLogger(__name__)


class TaskAction(Action):
    """ An Action that makes a callback to a Task.

    Note that this is a convenience class. Actions associated with a Task need
    not inherit TaskAction, although they must, of course, inherit Action.
    """

    #### TaskAction interface #################################################

    # The name of the Task method to call. By default, the on_perform function
    # will be called with the event.
    method = Str

    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event=None):
        """ Call the appropriate function.
        """
        if self.method != '':
            method = getattr(event.task, self.method, None)
            if method is not None:
                method(event)
            else:
                logger.error("Did not find implementation of %r on Task %r" %
                             (self.method, event.task.id))
        else:
            super(TaskAction, self).perform(event)
