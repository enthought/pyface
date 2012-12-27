#------------------------------------------------------------------------------
# Copyright (c) 2005-2013, Enthought, Inc.
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
#------------------------------------------------------------------------------
""" Helper functions to automatically generate unique IDs. """


from weakref import WeakKeyDictionary

class _ObjectCounter(object):
    """ Counts objects. """

    def __init__(self):
        self._objects_registry = WeakKeyDictionary()

    def get_count(self, obj):
        """ Return the number of times an object was seen.

        Objects must be hashable.

        """

        if obj in self._objects_registry:
            count = self._objects_registry[obj]
        else:
            count = 0

        return count

    def next_count(self, obj):
        """ Increase and return the number of times an object was seen.

        Objects must be hashable.

        """

        count = self.get_count(obj)
        self._objects_registry[obj] = count + 1
        return self._objects_registry[obj]

# Global object counter.
object_counter = _ObjectCounter()


def get_unique_id(object):
    """ Return a unique ID of the form ClassName_X, where X is an integer.

    It is only guaranteed that IDs are unique to a specific Python session, not
    across sessions.

    """

    class_ = object.__class__
    name = class_.__name__
    number = object_counter.next_count(class_)

    return name + '_' + str(number)
