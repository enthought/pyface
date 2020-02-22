# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A tool bar manager realizes itself in a tool palette control. """


# Import the toolkit specific version.
from pyface.toolkit import toolkit_object

ToolPaletteManager = toolkit_object(
    "action.tool_palette_manager:ToolPaletteManager"
)
