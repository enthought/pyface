# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Pyface 'DockWindow' support.

    This package provides a Pyface 'dockable' window component that allows
    child windows to be reorganized within the DockWindow using drag and drop.
    The component also allows multiple sub-windows to occupy the same
    sub-region of the DockWindow, in which case each sub-window appears as a
    separate notebook-like tab within the region.
"""

from .dock_window import DockWindow, DockWindowHandler

from .dock_sizer import (
    DockSizer,
    DockSection,
    DockRegion,
    DockControl,
    DockStyle,
    DOCK_LEFT,
    DOCK_RIGHT,
    DOCK_TOP,
    DOCK_BOTTOM,
    SetStructureHandler,
    add_feature,
    DockGroup,
)

from .idockable import IDockable

from .idock_ui_provider import IDockUIProvider

from .ifeature_tool import IFeatureTool

from .dock_window_shell import DockWindowShell

from .dock_window_feature import DockWindowFeature
