# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest

try:
    import wx
except ImportError:
    wx_available = False
else:
    from pyface.ui.wx.data_view.data_wrapper import DataWrapper
    wx_available = True


@unittest.skipUnless(wx_available, "Test requires wx")
class TestDataWrapper(unittest.TestCase):

    def test_get_mimedata(self):
        toolkit_data = wx.DataObjectComposite()
        text_data = wx.CustomDataObject(wx.DataFormat('text/plain'))
        text_data.SetData(b'hello world')
        toolkit_data.Add(text_data)
        data_wrapper = DataWrapper(toolkit_data=toolkit_data)
        self.assertEqual(data_wrapper.mimetypes(), {'text/plain'})
        self.assertEqual(data_wrapper.get_mimedata('text/plain'), b'hello world')

    def test_set_mimedata(self):
        data_wrapper = DataWrapper()
        toolkit_data = data_wrapper.toolkit_data
        data_wrapper.set_mimedata('text/plain', b'hello world')
        self.assertEqual(data_wrapper.mimetypes(), {'text/plain'})
        wx_format = wx.DataFormat('text/plain')
        self.assertTrue(toolkit_data.IsSupported(wx_format))
        text_data = toolkit_data.GetObject(wx_format)
        self.assertEqual(text_data.GetData(), b'hello world')

    def test_ignore_non_custom(self):
        toolkit_data = wx.DataObjectComposite()
        html_data = wx.HTMLDataObject()
        html_data.SetHTML("hello world")
        toolkit_data.Add(html_data)
        text_data = wx.CustomDataObject(wx.DataFormat('text/plain'))
        text_data.SetData(b'hello world')
        toolkit_data.Add(text_data)
        data_wrapper = DataWrapper(toolkit_data=toolkit_data)
        self.assertTrue('text/plain' in data_wrapper.mimetypes())
        self.assertEqual(data_wrapper.get_mimedata('text/plain'), b'hello world')
