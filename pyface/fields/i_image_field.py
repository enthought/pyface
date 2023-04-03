# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The image field interface. """

from traits.api import Any, HasTraits

from pyface.fields.i_field import IField
from pyface.ui_traits import Image


class IImageField(IField):
    """ The image field interface.

    This is for a field that edits a IImage value.
    """

    #: The current value of the image field
    value = Image()


class MImageField(HasTraits):
    """ Mixin class for ImageField implementations """

    #: The current value of the image field
    value = Image()

    #: The toolkit image to display
    _toolkit_value = Any()
