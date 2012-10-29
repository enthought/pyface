from pyface.i_drop_handler import IDropHandler
from traits.api import HasTraits, Callable, implements, List, Str

class BaseDropHandler(HasTraits):
    """ Basic drop handler
    """
    implements(IDropHandler)

    ### BaseDropHandler interface #############################################

    # Returns True if the current drop handler can handle the given drag event
    # occurring on the given target widget.
    on_can_handle = Callable

    # Performs drop action when drop event occurs on target widget.
    on_handle = Callable

    ### IDropHandler interface ################################################

    def can_handle_drop(self, event, target):
        return self.on_can_handle(event, target)

    def handle_drop(self, event, target):
        return self.on_handle(event, target)


class FileDropHandler(HasTraits):
    """ Class to handle backward compatible file drop events
    """
    implements(IDropHandler)

    ### FileDropHandler interface #############################################

    # supported extensions
    extensions = List(Str)

    # Called when file is opened. Takes single argument: path of file
    open_file = Callable

    ### IDropHandler interface ################################################

    def can_handle_drop(self, event, target):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(tuple(self.extensions)):
                    return True
        return False

    def handle_drop(self, event, target):
        for url in event.mimeData().urls():
            self.open_file(url.toLocalFile())
