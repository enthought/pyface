#-------------------------------------------------------------------------------
#
#  Copyright (c) 2005, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#  Author: David C. Morrill
#  Date:   10/18/2005
#
#-------------------------------------------------------------------------------

""" Pyface 'DockWindow' support.

    This package provides a Pyface 'dockable' window component that allows
    child windows to be reorganized within the DockWindow using drag and drop.
    The component also allows multiple sub-windows to occupy the same
    sub-region of the DockWindow, in which case each sub-window appears as a
    separate notebook-like tab within the region.
"""

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

from .dock_window import DockWindow, DockWindowHandler

from .dock_sizer import DockSizer, DockSection, DockRegion, DockControl, \
    DockStyle, DOCK_LEFT, DOCK_RIGHT, DOCK_TOP, DOCK_BOTTOM, \
    SetStructureHandler, add_feature, DockGroup

from .idockable import IDockable

from .idock_ui_provider import IDockUIProvider

from .ifeature_tool import IFeatureTool

from .dock_window_shell import DockWindowShell

from .dock_window_feature import DockWindowFeature
