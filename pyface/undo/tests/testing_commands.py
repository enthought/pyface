# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Int
from pyface.undo.api import AbstractCommand


class SimpleCommand(AbstractCommand):
    """ Simplest command possible operating on an integer. """

    name = "Increment by 1"

    data = Int()

    def do(self):
        self.redo()

    def redo(self):
        self.data += 1

    def undo(self):
        self.data -= 1


class UnnamedCommand(SimpleCommand):
    name = ""
