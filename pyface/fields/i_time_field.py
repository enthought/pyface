# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The time field interface. """

from datetime import time

from traits.api import HasTraits, Time

from pyface.fields.i_editable_field import IEditableField


class ITimeField(IEditableField):
    """ The time field interface.

    This is for a field that edits a datetime.time value.
    """

    #: The current value of the time field
    value = Time()


class MTimeField(HasTraits):
    """ Mixin class for TimeField implementations """

    #: The current value of the time field
    value = Time()

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait defaults --------------------------------------------------------

    def _value_default(self):
        return time.now()
