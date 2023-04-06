# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import csv
from functools import partial
from io import BytesIO, StringIO
import os
import json

from pyface.data_view.i_data_wrapper import DataFormat, text_format


# Scalar formats

def to_json(data, default=None):
    """ Serialize an object to a JSON bytestring.

    Parameters
    ----------
    data : Any
        The data to be serialized.
    default : Callable or None
        Callable that takes a Python object and returns a JSON-serializable
        data structure.

    Returns
    -------
    raw_data : bytes
        The serialized data as a bytestring.
    """
    str_data = json.dumps(data, default=default, separators=(',', ':'))
    return str_data.encode('utf-8')


def from_json(raw_data, object_hook=None):
    """ Deserialize a JSON bytestring.

    Parameters
    ----------
    raw_data : bytes
        The serialized JSON data as a byte string.
    object_hook : Callable
        Callable that takes a dictionary and returns an corresponding
        Python object.

    Returns
    -------
    data : Any
        The data extracted.
    """
    return json.loads(raw_data.decode('utf-8'), object_hook=object_hook)


#: The text/plain format with utf-8 encoding.
standard_text_format = text_format()

#: The text/html format with utf-8 encoding.
html_format = text_format(mimetype='text/html')

#: A generic JSON format.
json_format = DataFormat('application/json', to_json, from_json)


# 1D formats

def to_csv_row(data, delimiter=',', encoding='utf-8', **kwargs):
    """ Serialize a list to a single-row CSV bytestring.

    Parameters
    ----------
    data : list
        The list to be serialized.  Any elements which are not strings will
        be converted to strings by calling ``str()``.
    delimiter : str
        The CSV delimiter.
    encoding : str
        The encoding of the bytes
    **kwargs
        Additional arguments to csv.writer.

    Returns
    -------
    raw_data : bytes
        The serialized data as a bytestring.
    """
    fp = StringIO()
    writer = csv.writer(fp, delimiter=delimiter, **kwargs)
    writer.writerow(data)
    return fp.getvalue().encode(encoding)


def from_csv_row(raw_data, delimiter=',', encoding='utf-8', **kwargs):
    """ Deserialize the first row of a CSV bytestring as a list.

    Any rows beyond the first are ignored.

    Parameters
    ----------
    raw_data : bytes
        The serialized CSV data as a byte string.
    delimiter : str
        The CSV delimiter.
    encoding : str
        The encoding of the bytes
    **kwargs
        Additional arguments to csv.reader.

    Returns
    -------
    data : list of str
        The data extracted as a list of strings.
    """
    fp = StringIO(raw_data.decode(encoding))
    reader = csv.reader(fp, delimiter=delimiter, **kwargs)
    return next(reader)


def to_csv_column(data, delimiter=',', encoding='utf-8', **kwargs):
    """ Serialize a list to a single-column CSV bytestring.

    Parameters
    ----------
    data : list
        The list to be serialized.  Any elements which are not strings will
        be converted to strings by calling ``str()``.
    delimiter : str
        The CSV delimiter.
    encoding : str
        The encoding of the bytes
    **kwargs
        Additional arguments to csv.writer.

    Returns
    -------
    raw_data : bytes
        The serialized data as a bytestring.
    """
    fp = StringIO()
    writer = csv.writer(fp, delimiter=delimiter, **kwargs)
    for row in data:
        writer.writerow([row])
    return fp.getvalue().encode(encoding)


def from_csv_column(raw_data, delimiter=',', encoding='utf-8', **kwargs):
    """ Deserialize the first column of a CSV bytestring as a list.

    Any columns beyond the first are ignored.

    Parameters
    ----------
    raw_data : bytes
        The serialized CSV data as a byte string.
    delimiter : str
        The CSV delimiter.
    encoding : str
        The encoding of the bytes
    **kwargs
        Additional arguments to csv.reader.

    Returns
    -------
    data : list of str
        The data extracted as a list of strings.
    """
    fp = StringIO(raw_data.decode(encoding))
    reader = csv.reader(fp, delimiter=delimiter, **kwargs)
    return [row[0] for row in reader]


text_row_format = DataFormat(
    'text/plain',
    partial(to_csv_row, delimiter='\t', lineterminator=os.linesep),
    partial(from_csv_row, delimiter='\t'),
)
csv_row_format = DataFormat('text/csv', to_csv_row, from_csv_row)
text_column_format = DataFormat(
    'text/plain',
    partial(to_csv_column, delimiter='\t', lineterminator=os.linesep),
    partial(from_csv_column, delimiter='\t'),
)
csv_column_format = DataFormat('text/csv', to_csv_column, from_csv_column)


# 2D formats

def to_csv(data, delimiter=',', encoding='utf-8', **kwargs):
    """ Serialize a list of lists to a CSV bytestring.

    Parameters
    ----------
    data : list of lists
        The data to be serialized.  Any elements which are not strings will
        be converted to strings by calling ``str()``.
    delimiter : str
        The CSV delimiter.
    encoding : str
        The encoding of the bytes
    **kwargs
        Additional arguments to csv.writer.

    Returns
    -------
    raw_data : bytes
        The serialized data as a bytestring.
    """
    fp = StringIO()
    writer = csv.writer(fp, delimiter=delimiter, **kwargs)
    for row in data:
        writer.writerow(row)
    return fp.getvalue().encode(encoding)


def from_csv(raw_data, delimiter=',', encoding='utf-8', **kwargs):
    """ Deserialize a CSV bytestring.

    Parameters
    ----------
    raw_data : bytes
        The serialized CSV data as a byte string.
    delimiter : str
        The CSV delimiter.
    encoding : str
        The encoding of the bytes
    **kwargs
        Additional arguments to csv.reader.

    Returns
    -------
    data : list of list of str
        The data extracted as a list of lists of strings.
    """
    fp = StringIO(raw_data.decode(encoding))
    reader = csv.reader(fp, delimiter=delimiter, **kwargs)
    return list(reader)


def to_npy(data):
    """ Serialize an array to a bytestring using .npy format.

    Parameters
    ----------
    data : array-like
        The array to be serialized.

    Returns
    -------
    raw_data : bytes
        The serialized data as a bytestring.
    """
    import numpy as np

    data = np.atleast_2d(data)
    fp = BytesIO()
    np.save(fp, data, allow_pickle=False)
    return fp.getvalue()


def from_npy(raw_data):
    """ Deserialize a .npy-format bytestring.

    Parameters
    ----------
    raw_data : bytes
        The serialized CSV data as a byte string.

    Returns
    -------
    data : list of list of str
        The data extracted as a list of lists of strings.
    """
    import numpy as np

    fp = BytesIO(raw_data)
    return np.load(fp, allow_pickle=False)


table_format = DataFormat(
    'text/plain',
    partial(to_csv, delimiter='\t', lineterminator=os.linesep),
    partial(from_csv, delimiter='\t'),
)
csv_format = DataFormat('text/csv', to_csv, from_csv)
npy_format = DataFormat('application/x-npy', to_npy, from_npy)
