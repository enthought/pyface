# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Heading text. """

import warnings

from traits.api import HasTraits, Int, Interface, Str


class IHeadingText(Interface):
    """ Heading text. """

    # 'IHeadingText' interface ---------------------------------------------

    #: Heading level.
    #
    # fixme: Currently we ignore anything but one, but in future we could
    # have different visualizations based on the level.
    level = Int(1)

    #: The heading text.
    text = Str("Default")


class MHeadingText(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IHeadingText interface.
    """

    level = Int(1)

    text = Str("Default")

    def __init__(self, parent=None, **traits):
        """ Creates the heading text. """

        create = traits.pop("create", True)

        # Base class constructor.
        super().__init__(parent=parent, **traits)

        if create:
            # Create the widget's toolkit-specific control.
            self.create()
            warnings.warn(
                "automatic widget creation is deprecated and will be removed "
                "in a future Pyface version, use create=False and explicitly "
                "call create() for future behaviour",
                PendingDeprecationWarning,
            )
