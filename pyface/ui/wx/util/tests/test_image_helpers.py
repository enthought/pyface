# Copyright (c) 2005-2023, Enthought Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import unittest

import wx

from traits.testing.optional_dependencies import numpy as np, requires_numpy
from ..image_helpers import (
    bitmap_to_icon, bitmap_to_image, image_to_array, image_to_bitmap,
    array_to_image, AspectRatio, ScaleMode, resize_image, resize_bitmap,
)


class TestImageHelpers(unittest.TestCase):

    def test_image_to_bitmap(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)

        wxbitmap = image_to_bitmap(wximage)

        self.assertIsInstance(wxbitmap, wx.Bitmap)

    def test_bitmap_to_image(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wxbitmap = wximage.ConvertToBitmap()

        wximage = bitmap_to_image(wxbitmap)

        self.assertIsInstance(wximage, wx.Image)

    def test_bitmap_to_icon(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wxbitmap = wximage.ConvertToBitmap()

        wximage = bitmap_to_icon(wxbitmap)

        self.assertIsInstance(wximage, wx.Icon)

    def test_resize_image(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)

        wximage = resize_image(wximage, (128, 128))

        self.assertIsInstance(wximage, wx.Image)
        self.assertEqual(wximage.GetWidth(), 128)
        self.assertEqual(wximage.GetHeight(), 128)

    def test_resize_image_smooth(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)

        wximage = resize_image(wximage, (128, 128), mode=ScaleMode.smooth)

        self.assertIsInstance(wximage, wx.Image)
        self.assertEqual(wximage.GetWidth(), 128)
        self.assertEqual(wximage.GetHeight(), 128)

    def test_resize_image_constrain(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)

        wximage = resize_image(wximage, (128, 128), AspectRatio.keep_constrain)

        self.assertIsInstance(wximage, wx.Image)
        self.assertEqual(wximage.GetWidth(), 64)
        self.assertEqual(wximage.GetHeight(), 128)

    def test_resize_image_expand(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)

        wximage = resize_image(wximage, (128, 128), AspectRatio.keep_expand)

        self.assertIsInstance(wximage, wx.Image)
        self.assertEqual(wximage.GetWidth(), 128)
        self.assertEqual(wximage.GetHeight(), 256)

    def test_resize_bitmap(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wxbitmap = wximage.ConvertToBitmap()

        wxbitmap = resize_bitmap(wxbitmap, (128, 128))

        self.assertIsInstance(wxbitmap, wx.Bitmap)
        self.assertEqual(wxbitmap.GetWidth(), 128)
        self.assertEqual(wxbitmap.GetHeight(), 128)

    def test_resize_bitmap_smooth(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wxbitmap = wximage.ConvertToBitmap()

        wxbitmap = resize_bitmap(wxbitmap, (128, 128), mode=ScaleMode.smooth)

        self.assertIsInstance(wxbitmap, wx.Bitmap)
        self.assertEqual(wxbitmap.GetWidth(), 128)
        self.assertEqual(wxbitmap.GetHeight(), 128)

    def test_resize_bitmap_constrain(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wxbitmap = wximage.ConvertToBitmap()

        wxbitmap = resize_bitmap(wxbitmap, (128, 128), AspectRatio.keep_constrain)

        self.assertIsInstance(wxbitmap, wx.Bitmap)
        self.assertEqual(wxbitmap.GetWidth(), 64)
        self.assertEqual(wxbitmap.GetHeight(), 128)

    def test_resize_bitmap_expand(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wxbitmap = wximage.ConvertToBitmap()

        wxbitmap = resize_bitmap(wxbitmap, (128, 128), AspectRatio.keep_expand)

        self.assertIsInstance(wxbitmap, wx.Bitmap)
        self.assertEqual(wxbitmap.GetWidth(), 128)
        self.assertEqual(wxbitmap.GetHeight(), 256)


@requires_numpy
class TestArrayImageHelpers(unittest.TestCase):

    def test_image_to_array_rgb(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)

        array = image_to_array(wximage)

        self.assertEqual(array.shape, (32, 64, 4))
        self.assertEqual(array.dtype, np.dtype('uint8'))
        self.assertTrue(np.all(array[:, :, 3] == 0xff))
        self.assertTrue(np.all(array[:, :, 0] == 0x44))
        self.assertTrue(np.all(array[:, :, 1] == 0x88))
        self.assertTrue(np.all(array[:, :, 2] == 0xcc))

    def test_image_to_array_rgba(self):
        wximage = wx.Image(32, 64)
        wximage.SetRGB(wx.Rect(0, 0, 32, 64), 0x44, 0x88, 0xcc)
        wximage.InitAlpha()
        wximage.SetAlpha(np.full((32*64,), 0xee, dtype='uint8'))

        array = image_to_array(wximage)

        self.assertEqual(array.shape, (32, 64, 4))
        self.assertEqual(array.dtype, np.dtype('uint8'))
        self.assertTrue(np.all(array[:, :, 0] == 0x44))
        self.assertTrue(np.all(array[:, :, 1] == 0x88))
        self.assertTrue(np.all(array[:, :, 2] == 0xcc))
        self.assertTrue(np.all(array[:, :, 3] == 0xee))

    def test_array_to_image_rgb(self):
        array = np.empty((64, 32, 3), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88
        array[:, :, 2] = 0xcc

        wximage = array_to_image(array)

        self.assertEqual(wximage.GetWidth(), 32)
        self.assertEqual(wximage.GetHeight(), 64)
        self.assertFalse(wximage.HasAlpha())

    def test_array_to_image_rgba(self):
        array = np.empty((64, 32, 4), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88
        array[:, :, 2] = 0xcc
        array[:, :, 3] = 0xee

        wximage = array_to_image(array)

        self.assertEqual(wximage.GetWidth(), 32)
        self.assertEqual(wximage.GetHeight(), 64)
        self.assertTrue(wximage.HasAlpha())

    def test_array_to_image_bad_channels(self):
        array = np.empty((64, 32, 2), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88

        with self.assertRaises(ValueError):
            array_to_image(array)

    def test_array_to_image_bad_ndim(self):
        array = np.full((64, 32), 0x44, dtype='uint8')

        with self.assertRaises(ValueError):
            array_to_image(array)
