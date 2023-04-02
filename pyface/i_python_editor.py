# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" A widget for editing Python code. """


from traits.api import Bool, Event, HasTraits, Str

from pyface.i_layout_widget import ILayoutWidget
from pyface.key_pressed_event import KeyPressedEvent


class IPythonEditor(ILayoutWidget):
    """ A widget for editing Python code. """

    # 'IPythonEditor' interface --------------------------------------------

    #: Has the file in the editor been modified?
    dirty = Bool(False)

    #: The pathname of the file being edited.
    path = Str()

    #: Should line numbers be shown in the margin?
    show_line_numbers = Bool(True)

    # Events ----

    #: The contents of the editor has changed.
    changed = Event()

    #: A key has been pressed.
    key_pressed = Event(KeyPressedEvent)

    # ------------------------------------------------------------------------
    # 'IPythonEditor' interface.
    # ------------------------------------------------------------------------

    def load(self, path=None):
        """ Loads the contents of the editor.

        Parameters
        ----------
        path : str or None
            The path to the file to load.
        """

    def save(self, path=None):
        """ Saves the contents of the editor.

        Parameters
        ----------
        path : str or None
            The path to the file to save.
        """

    # FIXME v3: This is very dependent on the underlying implementation.
    def set_style(self, n, fore, back):
        """ Set the foreground and background colors for a particular style and
        set the font and size to default values.
        """

    def select_line(self, lineno):
        """ Selects the specified line.

        Parameters
        ----------
        lineno : int
            The line number to select.
        """


class MPythonEditor(HasTraits):
    """ The mixin class that contains common code for toolkit specific
    implementations of the IPythonEditor interface.

    Implements: _changed_path()
    """

    def _changed_path(self):
        """ Called when the path to the file is changed. """

        if self.control is not None:
            self.load()
