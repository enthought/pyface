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
# Date: 06/29/09
# ------------------------------------------------------------------------------


from traits.api import provides
from pyface.i_clipboard import IClipboard, BaseClipboard


@provides(IClipboard)
class Clipboard(BaseClipboard):
    """ A dummy clipboard implementationf for the null backend.
    """

    # ---------------------------------------------------------------------------
    #  'data' property methods:
    # ---------------------------------------------------------------------------

    def _get_has_data(self):
        return False

    # ---------------------------------------------------------------------------
    #  'object_data' property methods:
    # ---------------------------------------------------------------------------

    def _get_object_data(self):
        pass

    def _set_object_data(self, data):
        pass

    def _get_has_object_data(self):
        return False

    def _get_object_type(self):
        return ""

    # ---------------------------------------------------------------------------
    #  'text_data' property methods:
    # ---------------------------------------------------------------------------

    def _get_text_data(self):
        return False

    def _set_text_data(self, data):
        pass

    def _get_has_text_data(self):
        pass

    # ---------------------------------------------------------------------------
    #  'file_data' property methods:
    # ---------------------------------------------------------------------------

    def _get_file_data(self):
        pass

    def _set_file_data(self, data):
        pass

    def _get_has_file_data(self):
        return False
