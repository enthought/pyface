from traits.api import Interface


class IDropHandler(Interface):
    """ Interface for a drop event handler, which provides API to check if the
    drop can be handled or not, and then handle it if possible.
    """

    def can_handle_drop(self, event, target):
        """ Returns True if the current drop handler can handle the given drag
        event occurring on the given target widget.
        """

    def handle_drop(self, event, target):
        """ Performs drop action when drop event occurs on target widget.
        """
