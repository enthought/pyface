# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
#
# Author: Evan Patterson
# Date: 06/26/09
# ------------------------------------------------------------------------------

""" The interface for manipulating the toolkit clipboard.
"""

from collections.abc import Sequence

from traits.api import HasStrictTraits, Interface, Property


class IClipboard(Interface):
    """ The interface for manipulating the toolkit clipboard.
    """

    #: The type of data in the clipboard (string)
    data_type = Property

    #: Arbitrary Python data stored in the clipboard
    data = Property

    #: Arbitrary Python data is available in the clipboard
    has_data = Property

    #: Name of the class of object in the clipboard
    object_type = Property

    #: Python object data
    object_data = Property

    #: Python object data is available
    has_object_data = Property

    #: Text data
    text_data = Property

    #: Text data is available
    has_text_data = Property

    #: File name data
    file_data = Property

    #: File name data is available
    has_file_data = Property


class BaseClipboard(HasStrictTraits):
    """ An abstract base class that contains common code for toolkit specific
        implementations of IClipboard.
    """

    #: The type of data in the clipboard (string)
    data_type = Property

    #: Arbitrary Python data stored in the clipboard
    data = Property

    #: Arbitrary Python data is available in the clipboard
    has_data = Property

    #: Name of the class of object in the clipboard
    object_type = Property

    #: Python object data
    object_data = Property

    #: Python object data is available
    has_object_data = Property

    #: Text data
    text_data = Property

    #: Text data is available
    has_text_data = Property

    #: File name data
    file_data = Property

    #: File name data is available
    has_file_data = Property

    def _get_data(self):
        if self.has_text_data:
            return self.text_data
        if self.has_file_data:
            return self.file_data
        if self.has_object_data:
            return self.object_data
        return None

    def _set_data(self, data):
        if isinstance(data, str):
            self.text_data = data
        elif isinstance(data, Sequence):
            self.file_data = data
        else:
            self.object_data = data

    def _get_data_type(self):
        if self.has_text_data:
            return "str"
        if self.has_file_data:
            return "file"
        if self.has_object_data:
            return self.object_type
        return ""
