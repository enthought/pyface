# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
"""
Example Command-Line Application
================================

This is an example of an application used in purely command-line mode.
The application itself is trivial, but it demonstrates how to use the
Application class by overriding the `_run` method to perform the desired
computation.
"""


import argparse
from pyface.application import Application
from traits.api import Str


class HelloApplication(Application):
    """ Simple application example that greets a location. """

    # 'HelloApplication' traits -----------------------------------------------

    #: The location being greeted.
    location = Str("world")

    # 'Application' traits ----------------------------------------------------

    #: Human-readable application name
    name = "Hello Application"

    #: The application's globally unique identifier.
    id = "example_hello_application"

    def _run(self):
        super(HelloApplication, self)._run()
        print("Hello " + self.location)


def main():
    """ Hello application entrypoint. """
    app = HelloApplication()

    parser = argparse.ArgumentParser(description=app.description)
    parser.add_argument(
        "location",
        nargs="?",
        default=app.location,
        help="the location to greet",
    )
    parser.parse_args(namespace=app)

    app.run()


if __name__ == "__main__":
    main()
