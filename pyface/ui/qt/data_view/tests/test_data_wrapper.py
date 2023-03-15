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

from pyface.qt.QtCore import QMimeData
from pyface.ui.qt.data_view.data_wrapper import DataWrapper


class TestDataWrapper(TestCase):

    def test_get_mimedata(self):
        toolkit_data = QMimeData()
        toolkit_data.setData('text/plain', b'hello world')

        data_wrapper = DataWrapper(toolkit_data=toolkit_data)
        self.assertEqual(data_wrapper.mimetypes(), {'text/plain'})
        self.assertEqual(data_wrapper.get_mimedata('text/plain'), b'hello world')

    def test_set_mimedata(self):
        data_wrapper = DataWrapper()
        data_wrapper.set_mimedata('text/plain', b'hello world')
        toolkit_data = data_wrapper.toolkit_data

        self.assertEqual(set(toolkit_data.formats()), {'text/plain'})
        self.assertEqual(
            toolkit_data.data('text/plain').data(),
            b'hello world'
        )
