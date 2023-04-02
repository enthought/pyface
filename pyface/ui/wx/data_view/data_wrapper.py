# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from wx import CustomDataObject, DataFormat, DataObject, DataObjectComposite

from traits.api import Instance, provides

from pyface.data_view.i_data_wrapper import IDataWrapper, MDataWrapper


@provides(IDataWrapper)
class DataWrapper(MDataWrapper):
    """ WxPython implementaton of IDataWrapper.

    This wraps a DataObjectComposite which is assumed to contain a collection
    of CustomDataObjects that store data associated by mimetype.  Any other
    DataObjects in the DataObjectComposite are ignored.
    """

    #: We always have a a composite data object with custom data objects in it
    toolkit_data = Instance(
        DataObjectComposite,
        args=(),
        allow_none=False,
    )

    def mimetypes(self):
        """ Return a set of mimetypes holding data.

        Returns
        -------
        mimetypes : set of str
            The set of mimetypes currently storing data in the toolkit data
            object.
        """
        return {
            wx_format.GetId()
            for wx_format in self.toolkit_data.GetAllFormats()
        }

    def get_mimedata(self, mimetype):
        """ Get raw data for the given media type.

        Parameters
        ----------
        mimetype : str
            The mime media type to be extracted.

        Returns
        -------
        mimedata : bytes
            The mime media data as bytes.
        """
        wx_format = DataFormat(mimetype)
        if self.toolkit_data.IsSupported(wx_format):
            data_object = self.toolkit_data.GetObject(wx_format)
            if isinstance(data_object, CustomDataObject):
                return bytes(data_object.GetData())
        return None

    def set_mimedata(self, mimetype, raw_data):
        """ Set raw data for the given media type.

        Parameters
        ----------
        mimetype : str
            The mime media type to be extracted.
        mimedata : bytes
            The mime media data encoded as bytes..
        """
        wx_format = DataFormat(mimetype)
        if self.toolkit_data.IsSupported(wx_format, dir=DataObject.Set):
            data_object = self.toolkit_data.GetObject(wx_format)
        else:
            data_object = CustomDataObject(wx_format)
            self.toolkit_data.Add(data_object)
        data_object.SetData(raw_data)
