# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from unittest import TestCase

from pyface.data_view.i_data_wrapper import text_format
from pyface.data_view.data_wrapper import DataWrapper


class TestDataWrapper(TestCase):

    def test_instantiate(self):
        data_wrapper = DataWrapper()
        self.assertEqual(data_wrapper.mimetypes(), set())

    def test_mimedata_roundtrip(self):
        data_wrapper = DataWrapper()
        data_wrapper.set_mimedata('text/plain', b'hello world')
        result = data_wrapper.get_mimedata('text/plain')

        self.assertEqual(data_wrapper.mimetypes(), {'text/plain'})
        self.assertEqual(result, b'hello world')

    def test_mimedata_overwrite(self):
        data_wrapper = DataWrapper()
        data_wrapper.set_mimedata('text/plain', b'hello world')
        data_wrapper.set_mimedata('text/plain', b'hello mars')
        result = data_wrapper.get_mimedata('text/plain')

        self.assertEqual(data_wrapper.mimetypes(), {'text/plain'})
        self.assertEqual(result, b'hello mars')

    def test_set_format(self):
        data_wrapper = DataWrapper()
        format = text_format()

        data_wrapper.set_format(format, 'hëllø wørld')
        result = data_wrapper.get_mimedata('text/plain')

        self.assertEqual(data_wrapper.mimetypes(), {'text/plain'})
        self.assertEqual(result, 'hëllø wørld'.encode('utf-8'))
