# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for a simple 'About' dialog. """


from traits.api import HasTraits, Instance, List, Str


from pyface.i_dialog import IDialog
from pyface.image_resource import ImageResource


class IAboutDialog(IDialog):
    """ The interface for a simple 'About' dialog. """

    # 'IAboutDialog' interface ---------------------------------------------

    #: Additional strings to be added to the dialog.
    additions = List(Str)

    #: Additional copyright strings to be added above the standard ones.
    copyrights = List(Str)

    #: The image displayed in the dialog.
    image = Instance(ImageResource, ImageResource("about"))


class MAboutDialog(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IAboutDialog interface.
    """
