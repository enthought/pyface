# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""Demonstrate opening and saving a file with Pyface file dialogs."""

from pyface.api import CANCEL, OK, FileDialog


def main():
    """Open a Python file and choose where to save a copy."""
    wildcard = "Python files (*.py)|*.py|All files (*.*)|*.*"
    open_dialog = FileDialog(
        parent=None,
        title="Open a Python file",
        action="open",
        wildcard=wildcard,
    )
    if open_dialog.open() != OK:
        print("Open cancelled")
        return

    save_dialog = FileDialog(
        parent=None,
        title="Save a copy",
        action="save as",
        default_directory=open_dialog.directory,
        default_filename=f"copy_{open_dialog.filename}",
        wildcard=wildcard,
    )
    if save_dialog.open() != OK:
        print("Save cancelled")
        return

    print(f"Selected {open_dialog.path}")
    print(f"Save to {save_dialog.path}")


if __name__ == "__main__":
    main()
