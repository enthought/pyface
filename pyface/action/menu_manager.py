# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A toolkit-specific menu manager that realizes itself in a menu control.

- :attr:`~.MenuManager`
"""


# Import the toolkit specific version.
from pyface.toolkit import toolkit_object

MenuManager = toolkit_object("action.menu_manager:MenuManager")
