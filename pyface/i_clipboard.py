#------------------------------------------------------------------------------
# Copyright (c) 2009, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Evan Patterson
# Date: 06/26/09
#------------------------------------------------------------------------------

""" The interface for manipulating the toolkit clipboard.
"""

# ETS imports
from traits.api import HasStrictTraits, Interface, Property
from traitsui.ui_traits import SequenceTypes


class IClipboard(Interface):
    """ The interface for manipulating the toolkit clipboard.
    """

    data_type       = Property  # The type of data in the clipboard (string)
    data            = Property  # Arbitrary Python data
    has_data        = Property  # Arbitrary Python data is available

    object_type     = Property  # Name of the class of object in the clipboard
    object_data     = Property  # Python object data
    has_object_data = Property  # Python object data is available

    text_data       = Property  # Text data
    has_text_data   = Property  # Text data is available

    file_data       = Property  # File name data
    has_file_data   = Property  # File name data is available


class BaseClipboard(HasStrictTraits):
    """ An abstract base class that contains common code for toolkit specific
        implementations of IClipboard.
    """

    data_type       = Property  # The type of data in the clipboard (string)
    data            = Property  # Arbitrary Python data
    has_data        = Property  # Arbitrary Python data is available

    object_type     = Property  # Name of the class of object in the clipboard
    object_data     = Property  # Python object data
    has_object_data = Property  # Python object data is available

    text_data       = Property  # Text data
    has_text_data   = Property  # Text data is available

    file_data       = Property  # File name data
    has_file_data   = Property  # File name data is available

    def _get_data(self):
        if self.has_text_data:
            return self.text_data
        if self.has_file_data:
            return self.file_data
        if self.has_object_data:
            return self.object_data
        return None

    def _set_data(self, data):
        if isinstance(data, basestring):
            self.text_data = data
        elif type(data) in SequenceTypes:
            self.file_data = data
        else:
            self.object_data = data

    def _get_data_type ( self ):
        if self.has_text_data:
            return 'str'
        if self.has_file_data:
            return 'file'
        if self.has_object_data:
            return self.object_type
        return ''
