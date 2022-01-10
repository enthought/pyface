# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.api import FileDialog, OK


# display a file dialog for saving a Python file
dialog = FileDialog(parent=None, action="save as", wildcard="*.py")
if dialog.open() == OK:
    print(f"Save to {dialog.path}")
