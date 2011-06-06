# Standard library imports.
import logging

# Enthought library imports.
from pyface.action.api import Action
from traits.api import Any, Str

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
    # enabled. By default, the action is always enabled when an object is set.
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
            super(ListeningAction, self).perform(event)

    ###########################################################################
    # Protected interface.
    ###########################################################################

    def _get_attr(self, obj, name, default=None):
        try:
            for attr in name.split('.'):
                # Perform the access in the Trait name style: if the object is
                # None, assume it simply hasn't been initialized and don't show
                # the warning.
                if obj is None:
                    return default
                else:
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
        if self.enabled_name:
            if self.object:
                self.enabled = bool(self._get_attr(self.object, 
                                                   self.enabled_name, False))
            else:
                self.enabled = False
        else:
            self.enabled = bool(self.object)
