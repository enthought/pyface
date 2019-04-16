#------------------------------------------------------------------------------
# Copyright (c) 2017-19, Enthought, Inc.
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
""" The text field interface. """

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from traits.api import HasTraits, Int, Property, Range, Tuple

from pyface.fields.i_field import IField


class ISpinField(IField):
    """ The spin field interface.

    This is for spinners holding integer values.
    """

    #: The current value of the spinner
    value = Range(low='minimum', high='maximum')

    #: The bounds of the spinner
    bounds = Tuple(Int, Int)

    #: The minimum value
    minimum = Property(Int, depends_on='bounds')

    #: The maximum value
    maximum = Property(Int, depends_on='bounds')


class MSpinField(HasTraits):

    #: The current value of the spinner
    value = Range(low='minimum', high='maximum')

    #: The bounds for the spinner
    bounds = Tuple(Int, Int)

    #: The minimum value for the spinner
    minimum = Property(Int, depends_on='bounds')

    #: The maximum value for the spinner
    maximum = Property(Int, depends_on='bounds')

    # ------------------------------------------------------------------------
    # Private interface
    # ------------------------------------------------------------------------

    # Trait property handlers -----------------------------------------------

    def _get_minimum(self):
        return self.bounds[0]

    def _set_minimum(self, value):
        if value > self.maximum:
            self.bounds = (value, value)
        else:
            self.bounds = (value, self.maximum)
        if value > self.value:
            self.value = value

    def _get_maximum(self):
        return self.bounds[1]

    def _set_maximum(self, value):
        if value < self.minimum:
            self.bounds = (value, value)
        else:
            self.bounds = (self.minimum, value)
        if value < self.value:
            self.value = value
