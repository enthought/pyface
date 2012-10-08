""" The toolkit specific implementation of PyMimeData
"""


from pyface.qt import QtCore
from pyface.i_mimedata import IMimeData
from traits.api import HasTraits, implements

from cPickle import dumps, load, loads
from cStringIO import StringIO

class MimeTypes(object):
    """ Some predefined MIME Types for use in applications. """
    # The MIME type for instances.
    # Same as traitsui.qt4.clipboard.PyMimeData
    PYOBJ_PICKLE = 'application/x-ets-qt4-instance'
    PYOBJ_NOPICKLE = 'application/x-ets-qt4-instance-no-pickle'

    COLOR = 'application/x-color'
    HTML = 'text/html'
    TEXT = 'text/plain'
    URL = 'text/uri-list'

    # Other mime types used by canopy.
    PYTHON_CODE = 'text/x-ets-python-code'


#-------------------------------------------------------------------------------
#  'MimeData' class:
#-------------------------------------------------------------------------------

class MimeData(HasTraits):
    """ A MimeData container which can have data for multiple mime types.
    
    This can also wrap a Python instance.

    Parameters
    ----------
    obj - (optional) Python object to be stored as instance data.
    mimedata - native QMimeData (optional)
        the native mimedata type to store the data

    """

    implements(IMimeData)

    def __init__(self, obj=None, mimedata=None):
        """ Initialize the instance.
        """
        self._mimedata = QtCore.QMimeData()
        #if mimedata is not None:
        #    for format in mimedata.formats():
        #        self._mimedata.setData(format, mimedata.data(format))
        self.instance = obj

    @classmethod
    def from_mimedata(cls, md):
        """ Coerce a QMimeData instance to a MimeData instance if possible.
    
        If the QMimeData's python instance object is a MimeData, then
        that is returned.
        """
        if isinstance(md, cls):
            return md
    
        ret = cls(mimedata=md)
        # See if the data type is supported.
        if md.hasFormat(MimeTypes.PYOBJ_PICKLE):
            if issubclass(ret.instance_type, cls):
                return ret.instance
    
        return ret

    #### IMimeData interface #########################################################

    def _get_instance_type(self):
        """ The type (class) of the stored python instance.
        """
        if self.instance is not None:
            return self.instance.__class__

        try:
            if self._mimedata.hasFormat(MimeTypes.PYOBJ_PICKLE):
                return loads(str(self._mimedata.data(MimeTypes.PYOBJ_PICKLE)))
        except Exception as e:
            return None

    def _get_instance(self):
        """ The stored python object instance.
        """
        io = StringIO(str(self._mimedata.data(MimeTypes.PYOBJ_PICKLE)))

        # Skip the type.
        load(io)
        # Recreate the instance and cache it for further use.
        instance = load(io)
        return instance

    def _set_instance(self, obj):
        """ Set the instance data held by the mime data. """
        # This format (as opposed to using a single sequence) allows the
        # type to be extracted without unpickling the data itself.
        self.instance = obj
        if obj is None:
            return
        try:
            pdata = dumps(obj)
            self._mimedata.setData(MimeTypes.PYOBJ_PICKLE, dumps(obj.__class__) + pdata)
        except Exception as e:
            pdata = repr(obj)
            logger.info('Error while setting drop instance %s:%s. '\
                        'Cannot use from another application',
                         pdata, e)
            self._mimedata.setData(MimeTypes.PYOBJ_NOPICKLE, dumps(obj.__class__) + pdata)

    def _get_has_urls(self):
        """ Whether the mimedata has url list stored in it. """
        return self._mimedata.hasUrls()

    def _get_urls(self):
        """ The list of urls stored of file types. """
        qurls = self._mimedata.urls()
        ret = []
        for url in qurls:
            ret.append(url.toString())
        return ret

    def _set_urls(self, urls):
        """ Set urls of file types. """
        if isinstance(urls, basestring):
            self.urls = [urls]
        return self._mimedata.setUrls([QtCore.QUrl(url) for url in urls])

    def _get_local_paths(self):
        """ The list of local paths from url list, if any.
        """
        ret = []
        for url in self.urls:
            if url.scheme() == 'file':
                ret.append(url.toLocalFile())
        return ret

    def has_data(self, mimetype):
        """ Whether there is data for given mimetype. """
        return self._mimedata.hasFormat(mimetype)

    def get_data(self, mimetype):
        """ Return the data for given mimetype. """
        return self._mimedata.data(mimetype)

    def set_data(self, mimetype, data):
        """ Set the data for given mimetype. """
        self._mimedata.setData(mimetype, data)

    def formats(self):
        """ Return the mimetypes for which data is available. """
        return self._mimedata.formats()

    @staticmethod
    def to_local_path(url):
        """ Return a local path and from the given url. """
        return QtCore.QUrl(url).toLocalFile()
