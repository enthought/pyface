# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.api import DirectoryDialog, OK


# display a directory dialog for opening a directory
dialog = DirectoryDialog(parent=None)
if dialog.open() == OK:
    print(f"Open {dialog.path}")
