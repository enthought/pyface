# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Default base-class for resource factories. """


class ResourceFactory(object):
    """ Default base-class for resource factories. """

    # ------------------------------------------------------------------------
    # 'ResourceFactory' interface.
    # ------------------------------------------------------------------------

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        raise NotImplementedError()

    def image_from_data(self, data):
        """ Creates an image from the specified data. """

        raise NotImplementedError()
