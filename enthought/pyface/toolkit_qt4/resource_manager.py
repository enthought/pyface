#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

# Major package imports.
from PyQt4 import QtGui


class PyfaceResourceFactory_qt4(object):
    """ The PyfaceResourceFactory monkey patch for Qt4. """

    ###########################################################################
    # 'PyfaceResourceFactory' toolkit interface.
    ###########################################################################

    def _tk_pyfaceresourcefactory_image_from_file(self, filename):
        """ Creates an image from the data in the specified filename. """

        return QtGui.QPixmap(filename)

    def _tk_pyfaceresourcefactory_image_from_data(self, data):
        """ Creates an image from the specified data. """

        image = QtGui.QPixmap()
        image.loadFromData(data)

        return image
