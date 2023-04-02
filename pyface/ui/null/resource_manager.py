# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from pyface.resource.api import ResourceFactory


class PyfaceResourceFactory(ResourceFactory):
    """ The implementation of a shared resource manager. """

    # ------------------------------------------------------------------------
    # 'ResourceFactory' toolkit interface.
    # ------------------------------------------------------------------------

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """
        # Just return the data as a string for now.
        f = open(filename, "rb")
        data = f.read()
        f.close()

        return data

    def image_from_data(self, data):
        """ Creates an image from the specified data. """
        return data
