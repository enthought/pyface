#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

class Widget_qt4(object):
    """ The Widget monkey patch for Qt4. """

    ###########################################################################
    # 'Widget' toolkit interface.
    ###########################################################################

    def _tk_widget_destroy(self):
        """ Destroy the control. """

        # Assume that all controls are derived from QObject.
        self.control.deleteLater()
