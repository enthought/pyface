# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The interface for an image resource. """

from traits.api import HasStrictTraits, Instance

from pyface.i_image import IImage


class IPILImage(IImage):
    """ The interface for a image that wraps a PIL Image.
    """

    # 'IPILImage' interface --------------------------------------------

    #: The PIL Image instance.
    image = Instance("PIL.Image.Image")


class MPILImage(HasStrictTraits):
    """ The base implementation mixin for a image that wraps a PIL Image.
    """

    # 'IPILImage' interface --------------------------------------------

    #: The PIL Image instance.
    image = Instance("PIL.Image.Image")

    def __init__(self, image, **traits):
        super().__init__(image=image, **traits)
