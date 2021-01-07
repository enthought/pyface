# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


import math

from pyface.qt import QtCore, QtGui


class GutterWidget(QtGui.QWidget):

    min_width = 5
    background_color = QtGui.QColor(220, 220, 220)

    def sizeHint(self):
        return QtCore.QSize(self.min_width, 0)

    def paintEvent(self, event):
        """ Paint the line numbers.
        """
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), QtCore.Qt.lightGray)

    def wheelEvent(self, event):
        """ Delegate mouse wheel events to parent for seamless scrolling.
        """
        self.parent().wheelEvent(event)


class StatusGutterWidget(GutterWidget):
    """ Draws status markers
    """

    def __init__(self, *args, **kw):
        super(StatusGutterWidget, self).__init__(*args, **kw)

        self.error_lines = []
        self.warn_lines = []
        self.info_lines = []

    def sizeHint(self):
        return QtCore.QSize(10, 0)

    def paintEvent(self, event):
        """ Paint the line numbers.
        """
        painter = QtGui.QPainter(self)
        painter.fillRect(event.rect(), self.background_color)

        cw = self.parent()

        pixels_per_block = self.height() / float(cw.blockCount())

        for line in self.info_lines:
            painter.fillRect(
                QtCore.QRect(0, line * pixels_per_block, self.width(), 3),
                QtCore.Qt.green,
            )

        for line in self.warn_lines:
            painter.fillRect(
                QtCore.QRect(0, line * pixels_per_block, self.width(), 3),
                QtCore.Qt.yellow,
            )

        for line in self.error_lines:
            painter.fillRect(
                QtCore.QRect(0, line * pixels_per_block, self.width(), 3),
                QtCore.Qt.red,
            )


class LineNumberWidget(GutterWidget):
    """ Draw line numbers.
    """

    min_char_width = 4

    def fontMetrics(self):
        # QWidget's fontMetrics method does not provide an up to date
        # font metrics, just one corresponding to the initial font
        return QtGui.QFontMetrics(self.font)

    def set_font(self, font):
        self.font = font

    def digits_width(self):
        nlines = max(1, self.parent().blockCount())
        ndigits = max(
            self.min_char_width, int(math.floor(math.log10(nlines) + 1))
        )
        # QFontMetrics.width() is deprecated and Qt docs suggest using
        # horizontalAdvance() instead, but is only available since Qt 5.11
        if QtCore.__version_info__ >= (5, 11):
            width = max(
                self.fontMetrics().horizontalAdvance("0" * ndigits) + 3,
                self.min_width
            )
        else:
            width = max(
                self.fontMetrics().width("0" * ndigits) + 3, self.min_width
            )
        return width

    def sizeHint(self):
        return QtCore.QSize(self.digits_width(), 0)

    def paintEvent(self, event):
        """ Paint the line numbers.
        """
        painter = QtGui.QPainter(self)
        painter.setFont(self.font)
        painter.fillRect(event.rect(), self.background_color)

        cw = self.parent()
        block = cw.firstVisibleBlock()
        blocknum = block.blockNumber()
        top = (
            cw.blockBoundingGeometry(block)
            .translated(cw.contentOffset())
            .top()
        )
        bottom = top + int(cw.blockBoundingRect(block).height())

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                painter.setPen(QtCore.Qt.black)
                painter.drawText(
                    0,
                    top,
                    self.width() - 2,
                    self.fontMetrics().height(),
                    QtCore.Qt.AlignRight,
                    str(blocknum + 1),
                )
            block = block.next()
            top = bottom
            bottom = top + int(cw.blockBoundingRect(block).height())
            blocknum += 1
