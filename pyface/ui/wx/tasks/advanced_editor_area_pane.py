# Standard library imports.
import sys

# Enthought library imports.
from traits.api import provides

# Local imports.
from pyface.tasks.i_advanced_editor_area_pane import IAdvancedEditorAreaPane
from editor_area_pane import EditorAreaPane

###############################################################################
# 'AdvancedEditorAreaPane' class.
###############################################################################

@provides(IAdvancedEditorAreaPane)
class AdvancedEditorAreaPane(EditorAreaPane):
    """ The toolkit-specific implementation of an AdvancedEditorAreaPane.

    See the IAdvancedEditorAreaPane interface for API documentation.
    """
    
    # No additional functionality over the standard EditorAreaPane in wx yet.
