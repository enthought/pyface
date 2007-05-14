#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------

# Major package imports.
import wx


class MenuBarManager_wx(object):
    """ The MenuBarManager monkey patch for wx. """

    ###########################################################################
    # 'MenuManager' toolkit interface.
    ###########################################################################

    def _tk_menubarmanager_create_menu_bar(self, parent):
        """ Create a menu bar with the given parent. """

        return wx.MenuBar()

    def _tk_menubarmanager_add_menu(self, menu_bar, menu, name):
        """ Add a menu to a menu bar. """

        menu_bar.Append(menu, name)

        return

#### EOF ######################################################################
