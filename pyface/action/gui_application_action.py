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
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
""" Abstract base class for all application actions. """

import platform


from traits.api import Instance, Property, cached_property


from pyface.action.listening_action import ListeningAction

IS_WINDOWS = platform.system() == "Windows"


class GUIApplicationAction(ListeningAction):
    """ Abstract base class for GUI Application actions. """

    # 'ListeningAction' interface --------------------------------------------

    object = Property(observe="application")

    # 'WindowAction' interface -----------------------------------------------

    #: The application that the action is associated with.
    application = Instance("pyface.gui_application.GUIApplication")

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    def _get_object(self):
        return self.application

    def destroy(self):
        # Disconnect listeners to application and dependent properties.
        self.application = None
        super().destroy()


class ActiveWindowAction(GUIApplicationAction):
    """ Abstract base class for application active window actions. """

    # 'ListeningAction' interface --------------------------------------------

    object = Property(observe="application.active_window")

    # ------------------------------------------------------------------------
    # Protected interface.
    # ------------------------------------------------------------------------

    @cached_property
    def _get_object(self):
        if self.application is not None:
            return self.application.active_window


class CreateWindowAction(GUIApplicationAction):
    """ A standard 'New Window' menu action. """

    name = "New Window"
    accelerator = "Ctrl+N"

    def perform(self, event=None):
        window = self.application.create_window()
        self.application.add_window(window)


class ExitAction(GUIApplicationAction):
    """ A standard 'Quit' or 'Exit' menu action. """

    accelerator = "Alt+F4" if IS_WINDOWS else "Ctrl+Q"
    method = "exit"

    def _name_default(self):
        return ("Exit " if IS_WINDOWS else "Quit ") + self.application.name


class AboutAction(GUIApplicationAction):
    """ A standard 'About' dialog menu action. """

    method = "do_about"

    def _name_default(self):
        return "About " + self.application.name


class CloseActiveWindowAction(ActiveWindowAction):
    """ A standard 'Close window' menu action at the application level.

    This method closes the active window of the application.
    """

    name = "Close Window"
    accelerator = "Ctrl+W"
    method = "close"
