# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Test for pyface.api """

import unittest


class TestApi(unittest.TestCase):
    """ Test importable items in any environment."""

    def test_api_importable(self):
        # make sure api is importable with the most minimal
        # required dependencies, including in the absence of toolkit backends.
        from pyface.action import api   # noqa: F401

    def test_public_attrs(self):
        # make sure everything advertised by dir() is available except optional
        from pyface.action import api

        attrs = [
            name
            for name in dir(api)
            if not name.startswith('_')
        ]
        for attr in attrs:
            with self.subTest(attr=attr):
                self.assertIsNotNone(getattr(api, attr, None))
