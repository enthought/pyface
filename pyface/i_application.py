# (C) Copyright 2007-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" The application interface. """


# Enthought library imports.
from apptools.preferences.api import IPreferences
from traits.api import Event, Instance, Interface, Str, VetoableEvent

# Local imports.
from .application_event import ApplicationEvent


class IApplication(Interface):
    """ The application interface. """

    #: The application's globally unique identifier.
    id = Str

    #: The name of a directory (created for you) to which the application can
    #: read and write non-user accessible data, i.e. configuration information,
    #: preferences, etc.
    home = Str

    #: The name of a directory (created for you upon access) to which the
    #: application can read and write user-accessible data, e.g. projects
    #: created by the user.
    user_data = Str

    #: The root preferences node.
    preferences = Instance(IPreferences)

    #### Events ####

    #: Fired when the application is starting. This is the first thing that
    #: happens when the 'start' method is called.
    starting = VetoableEvent(ApplicationEvent)

    #: Fired when all plugins have been started.
    started = Event(ApplicationEvent)

    #: Fired when the plugin manager is stopping. This is the first thing that
    #: happens when the 'stop' method is called.
    stopping = VetoableEvent(ApplicationEvent)

    #: Fired when all plugins have been stopped.
    stopped = Event(ApplicationEvent)

    def run(self):
        """ Run the application.

        The same as::

          if application.start():
              application.stop()

        """
