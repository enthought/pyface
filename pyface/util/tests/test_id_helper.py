#
# Enthought product code
#
# (C) Copyright 2012 Enthought, Inc., Austin, TX
# All right reserved.
#
# This file is confidential and NOT open source.  Do not distribute.
#
""" Test the scripting tools. """


import unittest
from pyface.util.id_helper import get_unique_id, object_counter


class IDHelperTestCase(unittest.TestCase):
    """ Test the scripting tools. """

    #### Tests ################################################################

    def test_object_counter(self):

        from traits.api import WeakRef

        class Bogus(object):
            weak = WeakRef

        class Foo(object):
            foo = 3

        foo = Foo()

        self.assertEqual(object_counter.get_count(Bogus),  0)
        self.assertEqual(object_counter.next_count(Bogus), 1)
        self.assertEqual(object_counter.next_count(Bogus), 2)
        self.assertEqual(object_counter.get_count(Bogus),  2)
        self.assertEqual(object_counter.next_count(foo),  1)
        self.assertEqual(object_counter.next_count(Bogus), 3)

    def test_get_unique_id(self):

        class Bogus(object):
            pass

        bogus_1 = Bogus()
        bogus_2 = Bogus()

        self.assertEqual(get_unique_id(bogus_1), 'Bogus_1')
        self.assertEqual(get_unique_id(bogus_2), 'Bogus_2')

if __name__ == '__main__':
    unittest.main()

#### EOF ######################################################################
