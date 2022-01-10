# Copyright (c) 2005-2022, Enthought Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import unittest
import sys

from traits.testing.optional_dependencies import numpy as np, requires_numpy

from pyface.qt import qt_api
from pyface.qt.QtGui import QColor, QIcon, QImage, QPixmap

from ..image_helpers import (
    bitmap_to_icon,
    bitmap_to_image,
    image_to_array,
    image_to_bitmap,
    array_to_image,
    AspectRatio,
    ScaleMode,
    resize_image,
    resize_bitmap,
)


class TestImageHelpers(unittest.TestCase):
    def test_image_to_bitmap(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        qpixmap = image_to_bitmap(qimage)

        self.assertIsInstance(qpixmap, QPixmap)

    def test_bitmap_to_image(self):
        qpixmap = QPixmap(32, 64)
        qpixmap.fill(QColor(0x44, 0x88, 0xCC))

        qimage = bitmap_to_image(qpixmap)

        self.assertIsInstance(qimage, QImage)

    def test_bitmap_to_icon(self):
        qpixmap = QPixmap(32, 64)
        qpixmap.fill(QColor(0x44, 0x88, 0xCC))

        qimage = bitmap_to_icon(qpixmap)

        self.assertIsInstance(qimage, QIcon)

    def test_resize_image(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        qimage = resize_image(qimage, (128, 128))

        self.assertIsInstance(qimage, QImage)
        self.assertEqual(qimage.width(), 128)
        self.assertEqual(qimage.height(), 128)

    def test_resize_image_smooth(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        qimage = resize_image(qimage, (128, 128), mode=ScaleMode.smooth)

        self.assertIsInstance(qimage, QImage)
        self.assertEqual(qimage.width(), 128)
        self.assertEqual(qimage.height(), 128)

    def test_resize_image_constrain(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        qimage = resize_image(qimage, (128, 128), AspectRatio.keep_constrain)

        self.assertIsInstance(qimage, QImage)
        self.assertEqual(qimage.width(), 64)
        self.assertEqual(qimage.height(), 128)

    def test_resize_image_expand(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        qimage = resize_image(qimage, (128, 128), AspectRatio.keep_expand)

        self.assertIsInstance(qimage, QImage)
        self.assertEqual(qimage.width(), 128)
        self.assertEqual(qimage.height(), 256)

    def test_resize_bitmap(self):
        qpixmap = QPixmap(32, 64)
        qpixmap.fill(QColor(0x44, 0x88, 0xCC))

        qpixmap = resize_bitmap(qpixmap, (128, 128))

        self.assertIsInstance(qpixmap, QPixmap)
        self.assertEqual(qpixmap.width(), 128)
        self.assertEqual(qpixmap.height(), 128)

    def test_resize_bitmap_smooth(self):
        qpixmap = QPixmap(32, 64)
        qpixmap.fill(QColor(0x44, 0x88, 0xCC))

        qpixmap = resize_bitmap(qpixmap, (128, 128), mode=ScaleMode.smooth)

        self.assertIsInstance(qpixmap, QPixmap)
        self.assertEqual(qpixmap.width(), 128)
        self.assertEqual(qpixmap.height(), 128)

    def test_resize_bitmap_constrain(self):
        qpixmap = QPixmap(32, 64)
        qpixmap.fill(QColor(0x44, 0x88, 0xCC))

        qpixmap = resize_bitmap(
            qpixmap, (128, 128), AspectRatio.keep_constrain
        )

        self.assertIsInstance(qpixmap, QPixmap)
        self.assertEqual(qpixmap.width(), 64)
        self.assertEqual(qpixmap.height(), 128)

    def test_resize_bitmap_expand(self):
        qpixmap = QPixmap(32, 64)
        qpixmap.fill(QColor(0x44, 0x88, 0xCC))

        qpixmap = resize_bitmap(qpixmap, (128, 128), AspectRatio.keep_expand)

        self.assertIsInstance(qpixmap, QPixmap)
        self.assertEqual(qpixmap.width(), 128)
        self.assertEqual(qpixmap.height(), 256)


@requires_numpy
class TestArrayImageHelpers(unittest.TestCase):
    def test_image_to_array_rgb(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        array = image_to_array(qimage)

        self.assertEqual(array.shape, (64, 32, 4))
        self.assertEqual(array.dtype, np.dtype('uint8'))
        self.assertTrue(np.all(array[:, :, 3] == 0xFF))
        self.assertTrue(np.all(array[:, :, 0] == 0x44))
        self.assertTrue(np.all(array[:, :, 1] == 0x88))
        self.assertTrue(np.all(array[:, :, 2] == 0xCC))

    def test_image_to_array_rgba(self):
        qimage = QImage(32, 64, QImage.Format_ARGB32)
        qimage.fill(QColor(0x44, 0x88, 0xCC, 0xEE))

        array = image_to_array(qimage)

        self.assertEqual(array.shape, (64, 32, 4))
        self.assertEqual(array.dtype, np.dtype('uint8'))
        self.assertTrue(np.all(array[:, :, 0] == 0x44))
        self.assertTrue(np.all(array[:, :, 1] == 0x88))
        self.assertTrue(np.all(array[:, :, 2] == 0xCC))
        self.assertTrue(np.all(array[:, :, 3] == 0xEE))

    def test_image_to_array_bad(self):
        qimage = QImage(32, 64, QImage.Format_RGB30)
        qimage.fill(QColor(0x44, 0x88, 0xCC))

        with self.assertRaises(ValueError):
            image_to_array(qimage)

    @unittest.skipIf(
        qt_api == 'pyside2' and sys.platform == 'linux',
        "Pyside2 QImage.pixel returns signed integers on linux",
    )
    def test_array_to_image_rgb(self):
        array = np.empty((64, 32, 3), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88
        array[:, :, 2] = 0xCC

        qimage = array_to_image(array)

        self.assertEqual(qimage.width(), 32)
        self.assertEqual(qimage.height(), 64)
        self.assertEqual(qimage.format(), QImage.Format_RGB32)
        self.assertTrue(
            all(
                qimage.pixel(i, j) == 0xFF4488CC
                for i in range(32)
                for j in range(64)
            )
        )

    @unittest.skipIf(
        qt_api == 'pyside2' and sys.platform == 'linux',
        "Pyside2 QImage.pixel returns signed integers on linux",
    )
    def test_array_to_image_rgba(self):
        array = np.empty((64, 32, 4), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88
        array[:, :, 2] = 0xCC
        array[:, :, 3] = 0xEE

        qimage = array_to_image(array)

        self.assertEqual(qimage.width(), 32)
        self.assertEqual(qimage.height(), 64)
        self.assertEqual(qimage.format(), QImage.Format_ARGB32)
        self.assertTrue(
            all(
                qimage.pixel(i, j) == 0xEE4488CC
                for i in range(32)
                for j in range(64)
            )
        )

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
