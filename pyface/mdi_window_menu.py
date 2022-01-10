# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A menu that mimics the standard MDI window menu.

This is the menu that has the tile/cascade actions etc.

"""


from traits.api import Str


from .action.api import MenuManager, Separator, WindowAction


class Cascade(WindowAction):
    """ Cascades the windows. """

    # 'Action' interface ---------------------------------------------------

    name = Str("Ca&scade")
    tooltip = Str("Cascade the windows")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Cascades the windows. """

        self.window.control.Cascade()


class Tile(WindowAction):
    """ Tiles the windows horizontally. """

    # 'Action' interface ---------------------------------------------------

    name = Str("&Tile")
    tooltip = Str("Tile the windows")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Tiles the windows horizontally. """

        self.window.control.Tile()


class ArrangeIcons(WindowAction):
    """ Arranges the icons. """

    # 'Action' interface ---------------------------------------------------

    name = Str("&Arrange Icons")
    tooltip = Str("Arrange the icons")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Arranges the icons. """

        self.window.control.ArrangeIcons()


class Next(WindowAction):
    """ Activates the next window. """

    # 'Action' interface ---------------------------------------------------

    name = Str("&Next")
    tooltip = Str("Activate the next window")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Activates the next window. """

        self.window.control.ActivateNext()


class Previous(WindowAction):
    """ Activates the previous window. """

    # 'Action' interface ---------------------------------------------------

    name = Str("&Previous")
    tooltip = Str("Activate the previous window")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Activates the previous window. """

        self.window.control.ActivatePrevious()


class Close(WindowAction):
    """ Closes the current window. """

    # 'Action' interface ---------------------------------------------------

    name = Str("&Close")
    tooltip = Str("Close the current window")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Closes the current window. """

        page = self.window.control.GetActiveChild()
        if page is not None:
            page.Close()


class CloseAll(WindowAction):
    """ Closes all of the child windows. """

    # 'Action' interface ---------------------------------------------------

    name = Str("Close A&ll")
    tooltip = Str("Close all of the windows.")

    # ------------------------------------------------------------------------
    # 'Action' interface.
    # ------------------------------------------------------------------------

    def perform(self, event):
        """ Closes the child windows. """

        for page in self.window.control.GetChildren():
            page.Close()


class MDIWindowMenu(MenuManager):
    """ A menu that mimics the standard MDI window menus.

    This is the menu that has the tile/cascade actions etc.

    """

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __init__(self, window):
        """ Creates a new MDI window menu. """

        # Base class constructor.
        super().__init__(
            Cascade(window=window),
            Tile(window=window),
            Separator(),
            ArrangeIcons(window=window),
            Next(window=window),
            Previous(window=window),
            Close(window=window),
            CloseAll(window=window),
            name="&Window",
        )
