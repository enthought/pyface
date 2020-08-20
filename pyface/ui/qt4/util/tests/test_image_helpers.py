# Copyright (c) 2019, Enthought Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import absolute_import, unicode_literals

import unittest
import sys

try:
    import numpy as np
except Exception:
    np = None

from pyface.qt import is_qt4, qt_api
from pyface.qt.QtGui import QColor, QImage

from ..image_helpers import QImage_to_array, array_to_QImage


@unittest.skipIf(np is None, "NumPy is not available")
@unittest.skipIf(is_qt4, "QImage.pixelFormat not supported on Qt4")
class TestImageHelpers(unittest.TestCase):

    def test_qimage_to_array_rgb(self):
        qimage = QImage(32, 64, QImage.Format_RGB32)
        qimage.fill(QColor(0x44, 0x88, 0xcc))

        array = QImage_to_array(qimage)

        self.assertEqual(array.shape, (64, 32, 4))
        self.assertEqual(array.dtype, np.dtype('uint8'))
        self.assertTrue(np.all(array[:, :, 3] == 0xff))
        self.assertTrue(np.all(array[:, :, 0] == 0x44))
        self.assertTrue(np.all(array[:, :, 1] == 0x88))
        self.assertTrue(np.all(array[:, :, 2] == 0xcc))

    def test_qimage_to_array_rgba(self):
        qimage = QImage(32, 64, QImage.Format_ARGB32)
        qimage.fill(QColor(0x44, 0x88, 0xcc, 0xee))

        array = QImage_to_array(qimage)

        self.assertEqual(array.shape, (64, 32, 4))
        self.assertEqual(array.dtype, np.dtype('uint8'))
        self.assertTrue(np.all(array[:, :, 0] == 0x44))
        self.assertTrue(np.all(array[:, :, 1] == 0x88))
        self.assertTrue(np.all(array[:, :, 2] == 0xcc))
        self.assertTrue(np.all(array[:, :, 3] == 0xee))

    def test_qimage_to_array_bad(self):
        qimage = QImage(32, 64, QImage.Format_RGB30)
        qimage.fill(QColor(0x44, 0x88, 0xcc))

        with self.assertRaises(ValueError):
            array = QImage_to_array(qimage)

    @unittest.skipIf(
        qt_api == 'pyside2' and sys.platform == 'linux',
        "Pyside2 QImage.pixel returns signed integers on linux"
    )
    def test_array_to_qimage_rgb(self):
        array = np.empty((64, 32, 3), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88
        array[:, :, 2] = 0xcc

        qimage = array_to_QImage(array)

        self.assertEqual(qimage.width(), 32)
        self.assertEqual(qimage.height(), 64)
        self.assertEqual(qimage.format(), QImage.Format_RGB32)
        self.assertTrue(all(
            qimage.pixel(i, j) == 0xff4488cc
            for i in range(32) for j in range(64)
        ))

    @unittest.skipIf(
        qt_api == 'pyside2' and sys.platform == 'linux',
        "Pyside2 QImage.pixel returns signed integers on linux"
    )
    def test_array_to_qimage_rgba(self):
        array = np.empty((64, 32, 4), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88
        array[:, :, 2] = 0xcc
        array[:, :, 3] = 0xee

        qimage = array_to_QImage(array)

        self.assertEqual(qimage.width(), 32)
        self.assertEqual(qimage.height(), 64)
        self.assertEqual(qimage.format(), QImage.Format_ARGB32)
        self.assertTrue(all(
            qimage.pixel(i, j) == 0xee4488cc
            for i in range(32) for j in range(64)
        ))

    def test_array_to_qimage_bad_channels(self):
        array = np.empty((64, 32, 2), dtype='uint8')
        array[:, :, 0] = 0x44
        array[:, :, 1] = 0x88

        with self.assertRaises(ValueError):
            array_to_QImage(array)

    def test_array_to_qimage_bad_ndim(self):
        array = np.full((64, 32), 0x44, dtype='uint8')

        with self.assertRaises(ValueError):
            array_to_QImage(array)
