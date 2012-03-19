#------------------------------------------------------------------------------
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import re

from enaml.converters import Converter


class PhoneNumberConverter(Converter):
    """ A really dumb phone number converter.

    """
    all_digits = re.compile(r'[0-9]{10}$')

    dashes = re.compile(r'([0-9]{3})\-([0-9]{3})\-([0-9]{4})$')

    proper = re.compile(r'\(([0-9]{3})\)\ ([0-9]{3})\-([0-9]{4})$')

    def to_component(self, value):
        area, prefix, suffix = value
        return '(%s) %s-%s' % (area, prefix, suffix)

    def from_component(self, value):
        match = self.proper.match(value)
        if not match:
            match = self.dashes.match(value)
        if match:
            area = match.group(1)
            prefix = match.group(2)
            suffix = match.group(3)
            return (int(area), int(prefix), int(suffix))
        match = self.all_digits.match(value)
        if match:
            area = value[:3]
            prefix = value[3:6]
            suffix = value[6:10]
            return (int(area), int(prefix), int(suffix))
        raise ValueError('Unable to convert to valid phone number')

