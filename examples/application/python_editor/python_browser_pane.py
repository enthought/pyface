# Standard library imports.
import os.path

# Enthought library imports.
from pyface.tasks.api import TraitsDockPane
from traits.api import Event, File, List, Str
from traitsui.api import View, Item, FileEditor


class PythonBrowserPane(TraitsDockPane):
    """ A simple Python file browser pane.
    """

    # FileBrowserPane interface ----------------------------------------------

    # Fired when a file is double-clicked.
    activated = Event

    # The list of wildcard filters for filenames.
    filters = List(Str, ['*.py'])

    # The currently selected file.
    selected_file = File(os.path.expanduser('~'))

    # TaskPane interface -----------------------------------------------------

    id = 'example.python_browser_pane'
    name = 'File Browser'

    # The view used to construct the dock pane's widget.
    view = View(
        Item(
            'selected_file',
            editor=FileEditor(
                dclick_name='activated',
                filter_name='filters',
                root_path=os.path.expanduser('~'),
            ),
            style='custom',
            show_label=False
        ),
        resizable=True,
    )
