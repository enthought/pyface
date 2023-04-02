# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The perspective interface. """


from traits.api import Bool, Interface, List, Str, Tuple


from .perspective_item import PerspectiveItem


class IPerspective(Interface):
    """ The perspective interface. """

    # The perspective's unique identifier (unique within a workbench window).
    id = Str()

    # The perspective's name.
    name = Str()

    # The contents of the perspective.
    contents = List(PerspectiveItem)

    # The size of the editor area in this perspective. A value of (-1, -1)
    # indicates that the workbench window should choose an appropriate size
    # based on the sizes of the views in the perspective.
    editor_area_size = Tuple()

    # Is the perspective enabled?
    enabled = Bool()

    # Should the editor area be shown in this perspective?
    show_editor_area = Bool()

    # Methods -------------------------------------------------------------#

    def create(self, window):
        """ Create the perspective in a workbench window. """

    def show(self, window):
        """ Called when the perspective is shown in a workbench window. """
