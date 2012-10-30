#------------------------------------------------------------------------------
# Copyright (c) 2009, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Evan Patterson
# Date: 06/26/09
#------------------------------------------------------------------------------

# Standard library imports
from cStringIO import StringIO
from cPickle import dumps, load, loads
from types import NoneType

# System library imports
from pyface.qt import QtCore, QtGui

# ETS imports
from traits.api import implements
from pyface.i_clipboard import IClipboard, BaseClipboard

# Shortcuts
cb = QtGui.QApplication.clipboard()


#-------------------------------------------------------------------------------
#  'PyMimeData' class:
#-------------------------------------------------------------------------------

class PyMimeData(QtCore.QMimeData):
    """ The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    MIME_TYPE = 'application/x-ets-python-instance'
    NOPICKLE_MIME_TYPE = 'application/x-ets-python-instance-no-pickle'

    def __init__(self, data=None, pickle=True):
        """ Initialise the instance.
        """
        QtCore.QMimeData.__init__(self)
        self.set_instance(data, pickle)

    @classmethod
    def coerce(cls, md):
        """ Wrap a QMimeData or a python object to a PyMimeData.
        """
        # See if the data is already of the right type.  If it is then we know
        # we are in the same process.
        if isinstance(md, cls):
            return md

        # see if it is a QMimeData, and migrate all its data
        if isinstance(md, QtCore.QMimeData):
            nmd = cls()
            for format in md.formats():
                nmd.setData(format, md.data(format))
        else:
            # Arbitrary python object, wrap it into PyMimeData
            nmd = cls(md)

        return nmd

    has_format = QtCore.QMimeData.hasFormat
    has_text = QtCore.QMimeData.hasText
    set_text = QtCore.QMimeData.setText
    has_urls = QtCore.QMimeData.hasUrls
    set_data = QtCore.QMimeData.setData
    set_urls = QtCore.QMimeData.setUrls

    def urls(self):
        """ Overridden to return strings instead of QUrls """
        return [url.toString() for url in super(PyMimeData, self).urls()]


    def has_instance(self):
        return self._local_instance or self.has_format(self.MIME_TYPE)

    def instance(self):
        """ Return the instance.
        """
        if self._local_instance is not None:
            return self._local_instance

        io = StringIO(str(self.data(self.MIME_TYPE)))

        try:
            # Skip the type.
            load(io)

            # Recreate the instance.
            return load(io)
        except Exception:
            # Pickle raises more than just PickleError
            pass

        return None

    def instance_type(self):
        """ Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            if self.hasFormat(self.MIME_TYPE):
                return loads(str(self.data(self.MIME_TYPE)))
        except Exception:
            # Pickle raises more than just PickleError
            pass

        return NoneType

    def set_instance(self, data, pickle=True):
        # Keep a local reference to be returned if possible.
        self._local_instance = data

        if pickle:
            if data is not None:
                # We may not be able to pickle the data.
                try:
                    pdata = dumps(data)
                    # This format (as opposed to using a single sequence) allows
                    # the type to be extracted without unpickling the data.
                    self.setData(self.MIME_TYPE, dumps(data.__class__) + pdata)
                except Exception:
                    return

        else:
            self.setData(self.NOPICKLE_MIME_TYPE, str(id(data)))

    def local_paths(self):
        """ The list of local paths from url list, if any.
        """
        ret = []
        for url in super(PyMimeData, self).urls():
            if url.scheme() == 'file':
                ret.append(url.toLocalFile())
        return ret



# Custom MIME type representing python objects
PYTHON_TYPE = "python/object"


class Clipboard(BaseClipboard):

    implements(IClipboard)

    #---------------------------------------------------------------------------
    #  'data' property methods:
    #---------------------------------------------------------------------------

    def _get_has_data(self):
        return self.has_object_data or self.has_text_data or self.has_file_data

    #---------------------------------------------------------------------------
    #  'object_data' property methods:
    #---------------------------------------------------------------------------

    def _get_object_data(self):
        obj = None
        mime_data = cb.mimeData()
        if mime_data.hasFormat(PYTHON_TYPE):
            serialized_data = StringIO(str(mime_data.data(PYTHON_TYPE)))
            klass = load(serialized_data)
            obj = load(serialized_data)
        return obj

    def _set_object_data(self, data):
        mime_data = QtCore.QMimeData()
        serialized_data = dumps(data.__class__) + dumps(data)
        mime_data.setData(PYTHON_TYPE, QtCore.QByteArray(serialized_data))
        cb.setMimeData(mime_data)

    def _get_has_object_data(self):
        return cb.mimeData().hasFormat(PYTHON_TYPE)

    def _get_object_type(self):
        result = ''
        mime_data = cb.mimeData()
        if mime_data.hasFormat(PYTHON_TYPE):
            try:
                # We may not be able to load the required class:
                result = loads(str(mime_data.data(PYTHON_TYPE)))
            except:
                pass
        return result

    #---------------------------------------------------------------------------
    #  'text_data' property methods:
    #---------------------------------------------------------------------------

    def _get_text_data(self):
        return str(cb.text())

    def _set_text_data(self, data):
        cb.setText(data)

    def _get_has_text_data(self):
        return cb.mimeData().hasText()

    #---------------------------------------------------------------------------
    #  'file_data' property methods:
    #---------------------------------------------------------------------------

    def _get_file_data(self):
        mime_data = cb.mimeData()
        if mime_data.hasUrls():
            return [ str(url.toString()) for url in mime_data.urls() ]
        else:
            return []

    def _set_file_data(self, data):
        if isinstance(data, basestring):
            data = [ data ]
        mime_data = QtCore.QMimeData()
        mime_data.setUrls([ QtCore.QUrl(path) for path in data ])
        cb.setMimeData(mime_data)

    def _get_has_file_data (self):
        return cb.mimeData().hasUrls()
