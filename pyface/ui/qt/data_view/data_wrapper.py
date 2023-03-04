# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Instance, provides

from pyface.data_view.i_data_wrapper import IDataWrapper, MDataWrapper
from pyface.qt.QtCore import QMimeData


@provides(IDataWrapper)
class DataWrapper(MDataWrapper):
    """ Qt implementaton of IDataWrapper.

    This wraps a QMimeData in a straightforward way.
    """

    toolkit_data = Instance(QMimeData, args=(), allow_none=False)

    def mimetypes(self):
        """ Return a set of mimetypes holding data.

        Returns
        -------
        mimetypes : set of str
            The set of mimetypes currently storing data in the toolkit data
            object.
        """
        return set(self.toolkit_data.formats())

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
        return self.toolkit_data.data(mimetype).data()

    def set_mimedata(self, mimetype, raw_data):
        """ Set raw data for the given media type.

        Parameters
        ----------
        mimetype : str
            The mime media type to be extracted.
        mimedata : bytes
            The mime media data encoded as bytes..
        """
        return self.toolkit_data.setData(mimetype, raw_data)
