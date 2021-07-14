# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A widget for editing Python code. """


from traits.api import Bool, Event, Instance, File, Interface, Str
from pyface.tasks.i_editor import IEditor


from pyface.key_pressed_event import KeyPressedEvent


class IPythonEditor(IEditor):
    """ A widget for editing Python code. """

    # 'IPythonEditor' interface --------------------------------------------

    # Object being editor is a file
    obj = Instance(File)

    # The pathname of the file being edited.
    path = Str()

    # Should line numbers be shown in the margin?
    show_line_numbers = Bool(True)

    # Events ----

    # The contents of the editor has changed.
    changed = Event()

    # A key has been pressed.
    key_pressed = Event(KeyPressedEvent)

    # ------------------------------------------------------------------------
    # 'IPythonEditor' interface.
    # ------------------------------------------------------------------------

    def load(self, path=None):
        """ Loads the contents of the editor. """

    def save(self, path=None):
        """ Saves the contents of the editor. """

    def select_line(self, lineno):
        """ Selects the specified line. """
