# Copyright (c) 2014-18 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import argparse
from pyface.application import Application
from traits.api import Str


class HelloApplication(Application):
    """ Simple application example that greets a location. """

    #: The location being greeted.
    location = Str("world")

    def _run(self):
        super(HelloApplication, self)._run()
        print("Hello " + self.location)


def main():
    """ Hello application entrypoint. """
    app = HelloApplication()

    parser = argparse.ArgumentParser(description=app.description)
    parser.add_argument(
        'location',
        nargs='?',
        default=app.location,
        help="the location to greet"
    )
    parser.parse_args(namespace=app)

    app.run()


if __name__ == '__main__':
    main()
