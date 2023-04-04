# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from codecs import decode, encode
from functools import partial
from typing import Any as TAny, Callable as TCallable, NamedTuple

from traits.api import Any, HasStrictTraits, Interface


class DataFormat(NamedTuple):
    """ Information about a mimetype and serializers.

    Simple namedtuple-based class that stores the mimetype, serializer and
    deserializer together.
    """

    #: The mimetype of the data.
    mimetype: str

    #: A callable that serializes this format.  It should take an python
    #: object of a supported type, and return a bytestring.
    serialize: TCallable[[TAny], bytes]

    #: A callable that deserializes this format.  It should take a
    #: bytestring and return the extracted object.
    deserialize: TCallable[[bytes], TAny]


def text_format(encoding='utf-8', mimetype='text/plain'):
    """ DataFormat factory for text mimetypes.
    """
    return DataFormat(
        mimetype=mimetype,
        serialize=partial(encode, encoding=encoding),
        deserialize=partial(decode, encoding=encoding),
    )


class IDataWrapper(Interface):
    """ Wrapper around polymorphic toolkit data object containing mimedata.

    To support clipboard and drag and drop operations, toolkits need a way
    of generically representing data in multiple formats.  This is a wrapper
    class that provides a toolkit independent intreface to these classes
    which allow the exchange of data, with types specified by MIME types.
    """

    #: The toolkit data object.
    toolkit_data = Any()

    def mimetypes(self):
        """ Return a set of mimetypes holding data.

        Returns
        -------
        mimetypes : set of str
            The set of mimetypes currently storing data in the toolkit data
            object.
        """
        pass

    def has_format(self, format):
        """ Whether or not a particular format has available data.

        Parameters
        ----------
        format : DataFormat
            A data format object.

        Returns
        -------
        has_format : bool
            Whether or not there is data associated with that format in the
            underlying toolkit object.
        """
        raise NotImplementedError()

    def get_format(self, format):
        """ The decoded data associted with the format.

        Parameters
        ----------
        format : DataFormat
            A data format object.

        Returns
        -------
        data : Any
            The data decoded for the given format.
        """
        raise NotImplementedError()

    def set_format(self, format, data):
        """ Encode and set data for the format.

        Parameters
        ----------
        format : DataFormat
            A data format object.
        data : Any
            The data to be encoded and stored.
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

    def set_mimedata(self, mimetype, mimedata):
        """ Set raw data for the given media type.

        Parameters
        ----------
        mimetype : str
            The mime media type to be extracted.
        mimedata : bytes
            The mime media data encoded as bytes..
        """
        raise NotImplementedError()


class MDataWrapper(HasStrictTraits):
    """ Mixin class for DataWrappers.

    This provides standard methods for using DataFormat objects, but not the
    low-level communication with the underlying toolkit.
    """

    def has_format(self, format):
        """ Whether or not a particular format has available data.

        Parameters
        ----------
        format : DataFormat
            A data format object.

        Returns
        -------
        has_format : bool
            Whether or not there is data associated with that format in the
            underlying toolkit object.
        """
        return format.mimetype in self.mimetypes()

    def get_format(self, format):
        """ The decoded data associted with the format.

        Parameters
        ----------
        format : DataFormat
            A data format object.

        Returns
        -------
        data : Any
            The data decoded for the given format.
        """
        return format.deserialize(self.get_mimedata(format.mimetype))

    def set_format(self, format, data):
        """ Encode and set data for the format.

        Parameters
        ----------
        format : DataFormat
            A data format object.
        data : Any
            The data to be encoded and stored.
        """
        self.set_mimedata(format.mimetype, format.serialize(data))
