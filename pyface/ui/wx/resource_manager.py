# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


""" Enthought pyface package component
"""


import os
import tempfile
from io import BytesIO


import wx


from pyface.resource.api import ResourceFactory


class PyfaceResourceFactory(ResourceFactory):
    """ The implementation of a shared resource manager. """

    # ------------------------------------------------------------------------
    # 'ResourceFactory' toolkit interface.
    # ------------------------------------------------------------------------

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        # N.B 'wx.BITMAP_TYPE_ANY' tells wxPython to attempt to autodetect the
        # --- image format.
        return wx.Image(filename, wx.BITMAP_TYPE_ANY)

    def image_from_data(self, data, filename=None):
        """ Creates an image from the specified data. """
        return wx.Image(BytesIO(data))

        handle = None
        if filename is None:
            # If there is currently no way in wx to create an image from data,
            # we have write it out to a temporary file and then read it back in:
            handle, filename = tempfile.mkstemp()

        # Write it out...
        tf = open(filename, "wb")
        tf.write(data)
        tf.close()

        # ... and read it back in!  Lovely 8^()
        image = wx.Image(filename, wx.BITMAP_TYPE_ANY)

        # Remove the temporary file.
        if handle is not None:
            os.close(handle)
            os.unlink(filename)

        return image
