# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# (C) Copyright 2007 Riverbank Computing Limited
# This software is provided without warranty under the terms of the BSD license.
# However, when used with the GPL version of PyQt the additional terms described in the PyQt GPL exception also apply


from pyface.qt import QtCore, QtGui, QtSvg


from pyface.resource.api import ResourceFactory


class PyfaceResourceFactory(ResourceFactory):
    """ The implementation of a shared resource manager. """

    # ------------------------------------------------------------------------
    # 'ResourceFactory' interface.
    # ------------------------------------------------------------------------

    def image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        # Although QPixmap can load SVG directly, it does not respect the
        # default size, so we use a QSvgRenderer to get the default size.
        if filename.endswith((".svg", ".SVG")):
            renderer = QtSvg.QSvgRenderer(filename)
            pixmap = QtGui.QPixmap(renderer.defaultSize())
            pixmap.fill(QtCore.Qt.GlobalColor.transparent)
            painter = QtGui.QPainter(pixmap)
            renderer.render(painter)

        else:
            pixmap = QtGui.QPixmap(filename)

        return pixmap

    def image_from_data(self, data, filename=None):
        """ Creates an image from the specified data. """

        image = QtGui.QPixmap()
        image.loadFromData(data)

        return image
