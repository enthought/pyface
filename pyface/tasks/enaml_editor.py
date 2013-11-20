# local imports
from pyface.tasks.editor import Editor
from pyface.tasks.enaml_pane import EnamlPane


class EnamlEditor(EnamlPane, Editor):
    """ Create an Editor for Enaml Components. """
