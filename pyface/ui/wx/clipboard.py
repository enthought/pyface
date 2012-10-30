#------------------------------------------------------------------------------
# Copyright (c) 2009, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------

# Standard library imports
from cStringIO import StringIO
from cPickle import dumps, load, loads

# System library imports
import wx

# ETS imports
from traits.api import implements
from pyface.i_clipboard import IClipboard, BaseClipboard
from types import NoneType

# Data formats
PythonObjectFormat = wx.CustomDataFormat('application/x-ets-python-instance')
PythonNopickleObjectFormat = wx.CustomDataFormat(
                                 'application/x-ets-python-instance-no-pickle')
PythonObject = wx.CustomDataFormat('PythonObject')

TextFormat         = wx.DataFormat(wx.DF_TEXT)
FileFormat         = wx.DataFormat(wx.DF_FILENAME)
OtherObjectFormat = wx.CustomDataFormat('application/x-extra-formats')

# Shortcuts
cb           = wx.TheClipboard


#-------------------------------------------------------------------------------
#  'PyMimeData' class:
#-------------------------------------------------------------------------------

class PyMimeData(wx.DataObjectComposite):
    """ The PyMimeData wraps a Python instance as MIME data.
    """
    # The MIME type for instances.
    PYTHON_Object = 'application/x-ets-python-instance'
    NOPICKLE_MIME_TYPE = 'application/x-ets-python-instance-no-pickle'
    URI_LIST = 'text/uri-list'

    def __init__(self, data=None, pickle=True):
        """ Initialise the instance.
        """
        super(PyMimeData, self).__init__()
        self.set_instance(data, pickle)

    @classmethod
    def coerce(cls, do):
        """ Wrap a DataObject or a python object to a PyMimeData.
        """
        # See if the data is already of the right type.  If it is then we know
        # we are in the same process.
        if isinstance(do, cls):
            return do

        # see if it is a QMimeData, and migrate all its data
        if isinstance(do, wx.DataObject):
            nmd = cls()
            for format in do.GetAllFormats():
                nmd.SetData(wx.DataFormat(format), do.GetDataHere(format))
        else:
            # Arbitrary python object, wrap it into PyMimeData
            nmd = cls(do)

        return nmd

    def formats(self):
        formats = []
        for format in self.AllFormats():
            if self.GetDataHere(format) is not None:
                formats.append(format.GetId())

    def has_data(self, format):
        return self.GetDataHere(wx.DataFormat(format)) is not None

    def data(self, format):
        return self.GetDataHere(wx.DataFormat(format))

    def set_data(self, format, data):
        wformat = wx.DataFormat(format)
        if not self.IsSupported(wformat):
            self.Add(wformat)
        self.SetData(wformat, data)

    def has_text(self):
        return self.has_format(TextFormat)

    def text(self):
        return self.GetDataHere(TextFormat)

    def set_text(self, text):
        self.set_data(wx.DF_TEXT, text)

    def has_urls(self):
        return self.has_format(wx.DF_FILENAME)

    def urls(self):
        return self.GetDataHere(FileFormat)

    def set_urls(self, urls):
        self.set_data(wx.DF_FILENAME, urls)

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

        return NoneType

    def instance_type(self):
        """ Return the type of the instance.
        """
        if self._local_instance is not None:
            return self._local_instance.__class__

        try:
            if self.has_format(self.MIME_TYPE):
                return loads(str(self.data(self.MIME_TYPE)))
        except Exception:
            # Pickle raises more than just PickleError
            pass

        return None

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
        for url in self.urls():
            if url.startswith('file://'):
                ret.append(url[7:])
        return ret



class Clipboard(BaseClipboard):

    implements(IClipboard)

    #---------------------------------------------------------------------------
    #  'data' property methods:
    #---------------------------------------------------------------------------

    def _get_has_data(self):
        result = False
        if cb.Open():
            result = (cb.IsSupported(TextFormat) or
                      cb.IsSupported(FileFormat) or
                      cb.IsSupported(PythonObjectFormat))
            cb.Close()
        return result

    #---------------------------------------------------------------------------
    #  'object_data' property methods:
    #---------------------------------------------------------------------------

    def _get_object_data(self):
        result = None
        if cb.Open():
            try:
                if cb.IsSupported(PythonObjectFormat):
                    cdo = wx.CustomDataObject(PythonObjectFormat)
                    if cb.GetData(cdo):
                        file   = StringIO(cdo.GetData())
                        klass  = load(file)
                        result = load(file)
            finally:
                cb.Close()
        return result

    def _set_object_data(self, data):
        if cb.Open():
            try:
                cdo = wx.CustomDataObject(PythonObjectFormat)
                cdo.SetData(dumps(data.__class__) + dumps(data))
                # fixme: There seem to be cases where the '-1' value creates
                # pickles that can't be unpickled (e.g. some TraitDictObject's)
                #cdo.SetData(dumps(data, -1))
                cb.SetData(cdo)
            finally:
                cb.Close()
                cb.Flush()

    def _get_has_object_data(self):
        return self._has_this_data(PythonObjectFormat)

    def _get_object_type(self):
        result = ''
        if cb.Open():
            try:
                if cb.IsSupported(PythonObjectFormat):
                    cdo = wx.CustomDataObject(PythonObjectFormat)
                    if cb.GetData(cdo):
                        try:
                            # We may not be able to load the required class:
                            result = loads(cdo.GetData())
                        except:
                            pass
            finally:
                cb.Close()
        return result

    #---------------------------------------------------------------------------
    #  'text_data' property methods:
    #---------------------------------------------------------------------------

    def _get_text_data(self):
        result = ''
        if cb.Open():
            if cb.IsSupported(TextFormat):
                tdo = wx.TextDataObject()
                if cb.GetData(tdo):
                    result = tdo.GetText()
            cb.Close()
        return result

    def _set_text_data(self, data):
        if cb.Open():
            cb.SetData(wx.TextDataObject(str(data)))
            cb.Close()
            cb.Flush()

    def _get_has_text_data(self):
        return self._has_this_data(TextFormat)

    #---------------------------------------------------------------------------
    #  'file_data' property methods:
    #---------------------------------------------------------------------------

    def _get_file_data(self):
        result = []
        if cb.Open():
            if cb.IsSupported(FileFormat):
                tfo = wx.FileDataObject()
                if cb.GetData(tfo):
                    result = tfo.GetFilenames()
            cb.Close()
        return result

    def _set_file_data(self, data):
        if cb.Open():
            tfo = wx.FileDataObject()
            if isinstance(data, basestring):
                tfo.AddFile(data)
            else:
                for filename in data:
                    tfo.AddFile(filename)
            cb.SetData(tfo)
            cb.Close()
            cb.Flush()

    def _get_has_file_data(self):
        return self._has_this_data(FileFormat)

    #---------------------------------------------------------------------------
    #  Private helper methods:
    #---------------------------------------------------------------------------

    def _has_this_data(self, format):
        result = False
        if cb.Open():
            result = cb.IsSupported(format)
            cb.Close()
        return result
