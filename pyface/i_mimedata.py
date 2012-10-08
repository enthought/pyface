""" The interface for manipulating the toolkit mimedata.
"""
from traits.api import Interface

class IMimeData(Interface):
    """ A MimeData container which can have data for multiple mime types.
    
    This can also wrap a Python instance.

    """
    # stored python object instance.
    instance = Property(instance_type)

    # type of the stored python instance
    instance_type = Property(depends_on=instance)

    # whether the mimedata has url list stored in it.
    has_urls = Property(Bool)

    # list of urls stored of file types
    urls = Property(List(Str))

    # local paths corresponding to the list of urls
    local_paths = Property(List(Str), depends_on=urls)

    def has_data(self, mimetype):
        """ Whether there is data for given mimetype. """

    def get_data(self, mimetype):
        """ Return the data for given mimetype. """

    def set_data(self, mimetype, data):
        """ Set the data for given mimetype. """

    def formats(self):
        """ Return the mimetypes for which data is available. """
