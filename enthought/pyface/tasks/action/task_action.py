# Standard library imports.
import logging

# Enthought library imports.
from enthought.pyface.action.api import Action
from enthought.pyface.tasks.api import Task
from enthought.traits.api import Any, Instance, Property, Str, cached_property

# Logging.
logger = logging.getLogger(__name__)


class ListeningAction(Action):
    """ An Action that listens and makes a callback to an object.
    """
    
    #### ListeningAction interface ############################################
    
    # The (extended) name of the method to call. By default, the on_perform
    # function will be called with the event.
    method = Str

    # The (extended) name of the attribute that determines whether the action is
    # enabled. By default, the action is always enabled.
    enabled_name = Str

    # The object to which the names above apply.
    object = Any
    
    ###########################################################################
    # 'Action' interface.
    ###########################################################################

    def perform(self, event=None):
        """ Call the appropriate function.
        """
        if self.method != '':
            method = self._get_attr(self.object, self.method)
            if method:
                method()
        else:
            super(TaskAction, self).perform(event)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_attr(self, obj, name, default=None):
        for attr in name.split('.'):
            try:
                obj = getattr(obj, attr)
            except AttributeError:
                logger.error("Did not find name %r on %r" % (attr, obj))
                return default
        return obj

    #### Trait change handlers ################################################

    def _enabled_name_changed(self, old, new):
        obj = self.object
        if obj is not None:
            if old:
                obj.on_trait_change(self._enabled_update, old, remove=True)
            if new:
                obj.on_trait_change(self._enabled_update, new)
            self._enabled_update()

    def _object_changed(self, old, new):
        name = self.enabled_name
        if name:
            if old:
                old.on_trait_change(self._enabled_update, name, remove=True)
            if new:
                new.on_trait_change(self._enabled_update, name)
            self._enabled_update()

    def _enabled_update(self):
        self.enabled = self._get_attr(self.object, self.enabled_name, False)


class TaskAction(ListeningAction):
    """ An Action that makes a callback to a Task.

    Note that this is a convenience class. Actions associated with a Task need
    not inherit TaskAction, although they must, of course, inherit Action.
    """

    #### ListeningAction interface ############################################

    # Use the Task as the object.
    object = Property(depends_on='task')

    #### TaskAction interface #################################################

    # The Task with which the action is associated. Set by the framework.
    task = Instance(Task)
    
    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_object(self):
        return self.task
    

class CentralPaneAction(TaskAction):
    """ An Action that makes a callback to a Task's central pane.
    """
    
    ###########################################################################
    # Protected interface.
    ###########################################################################

    @cached_property
    def _get_object(self):
        if self.task:
            return self.task.window.get_central_pane(self.task)
        return None
