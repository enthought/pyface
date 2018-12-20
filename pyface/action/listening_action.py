# Copyright (c) 2005-2018, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>

# Standard library imports.
import logging

# Enthought library imports.
from pyface.action.action import Action
from traits.api import Any, Str

# Logging.
logger = logging.getLogger(__name__)


class ListeningAction(Action):
    """ An Action that listens and makes a callback to an object.
    """

    # ListeningAction interface ----------------------------------------------

    #: The (extended) name of the method to call. By default, the on_perform
    #: function will be called with the event.
    method = Str

    #: The (extended) name of the attribute that determines whether the action
    #: is enabled. By default, the action is always enabled when an object is
    #: set.
    enabled_name = Str

    #: The (extended) name of the attribute that determines whether the action
    #: is visible. By default, the action is always visible.
    visible_name = Str

    #: The object to which the names above apply.
    object = Any

    # -------------------------------------------------------------------------
    # 'Action' interface.
    # -------------------------------------------------------------------------

    def destroy(self):
        """ Called when the action is no longer required.

        Removes all the task listeners.
        """

        if self.object:
            self.object.on_trait_change(
                self._enabled_update, self.enabled_name, remove=True
            )
            self.object.on_trait_change(
                self._visible_update, self.visible_name, remove=True
            )

    def perform(self, event=None):
        """ Call the appropriate function.

        This looks for a method to call based on the extended method name
        stored in the :py:attr:`method` trait.  If the method is empty, then
        this follows the usual Action method resolution.
        """
        if self.method != '':
            method = self._get_attr(self.object, self.method)
            if method:
                method()
        else:
            super(ListeningAction, self).perform(event)

    # -------------------------------------------------------------------------
    # Protected interface.
    # -------------------------------------------------------------------------

    def _get_attr(self, obj, name, default=None):
        """ Perform an extended look up of a dotted name. """
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

    # Trait change handlers --------------------------------------------------

    def _enabled_name_changed(self, old, new):
        obj = self.object
        if obj is not None:
            if old:
                obj.on_trait_change(self._enabled_update, old, remove=True)
            if new:
                obj.on_trait_change(self._enabled_update, new)
        self._enabled_update()

    def _visible_name_changed(self, old, new):
        obj = self.object
        if obj is not None:
            if old:
                obj.on_trait_change(self._visible_update, old, remove=True)
            if new:
                obj.on_trait_change(self._visible_update, new)
        self._visible_update()

    def _object_changed(self, old, new):
        for kind in ('enabled', 'visible'):
            method = getattr(self, '_%s_update' % kind)
            name = getattr(self, '%s_name' % kind)
            if name:
                if old:
                    old.on_trait_change(method, name, remove=True)
                if new:
                    new.on_trait_change(method, name)
            method()

    def _enabled_update(self):
        if self.enabled_name:
            if self.object:
                self.enabled = bool(
                    self._get_attr(self.object, self.enabled_name, False)
                )
            else:
                self.enabled = False
        else:
            self.enabled = bool(self.object)

    def _visible_update(self):
        if self.visible_name:
            if self.object:
                self.visible = bool(
                    self._get_attr(self.object, self.visible_name, False)
                )
            else:
                self.visible = False
        else:
            self.visible = True
