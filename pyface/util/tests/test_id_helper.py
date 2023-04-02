# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Test the scripting tools. """


import unittest
from pyface.util.id_helper import get_unique_id, object_counter


class IDHelperTestCase(unittest.TestCase):
    """ Test the scripting tools. """

    # Tests ----------------------------------------------------------------

    def test_object_counter(self):

        from traits.api import WeakRef

        class Bogus(object):
            weak = WeakRef

        class Foo(object):
            foo = 3

        foo = Foo()

        self.assertEqual(object_counter.get_count(Bogus), 0)
        self.assertEqual(object_counter.next_count(Bogus), 1)
        self.assertEqual(object_counter.next_count(Bogus), 2)
        self.assertEqual(object_counter.get_count(Bogus), 2)
        self.assertEqual(object_counter.next_count(foo), 1)
        self.assertEqual(object_counter.next_count(Bogus), 3)

    def test_get_unique_id(self):
        class Bogus(object):
            pass

        bogus_1 = Bogus()
        bogus_2 = Bogus()

        self.assertEqual(get_unique_id(bogus_1), "Bogus_1")
        self.assertEqual(get_unique_id(bogus_2), "Bogus_2")
