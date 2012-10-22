from pyface.i_drop_handler import IDropHandler
from traits.api import HasTraits, Callable, implements, List, Str

class BaseDropHandler(HasTraits):
    """ Basic drop handler
    """
    implements(IDropHandler)

    # Returns True if the current drop handler can handle the given drag event 
    # occurring on the given target widget.
    on_can_handle = Callable

    # Performs drop action when drop event occurs on target widget. Returns True 
    # if it successfully handled the event, otherwise False. Does nothing if it 
    # couldn't handle the event.
    on_handle = Callable

    ### IDropHandler interface ##################################################

    def can_handle_drop(self, event, target):
        return self.on_can_handle(event, target)

    def handle_drop(self, event, target):
        return self.on_handle(event, target)


class FileDropHandler(BaseDropHandler):
    """ Class to handle backward compatible file drop events
    """
    # supported extensions
    extensions = List(Str)

    # Called when file is opened. Takes single argument: path of file
    open_file = Callable

    def can_handle_drop(self, event, target):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if file_path.endswith(tuple(self.extensions)):
                    return True
        return False

    def handle_drop(self, event, target):
        if not self.can_handle_drop(event, target):
            return False

        accepted = False
        for url in event.mimeData().urls():
            self.open_file(url.toLocalFile())
            accepted = True
        return accepted