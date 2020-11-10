# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
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

    def test_api_importable(self):
        # make sure api is importable with the most minimal
        # required dependencies, including in the absence of toolkit backends.
        from pyface import api   # noqa: F401
