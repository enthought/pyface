#------------------------------------------------------------------------------
# Copyright (c) 2012, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#------------------------------------------------------------------------------
""" This class defines a mimedata object for data transfers via drag-drop.

The API is as follows:

class PyMimeData:
    formats() -> list(str) : list of data formats available
    data(str) -> str : return data of specified format or None
    has_data(str) -> bool : whether data is available in specified format

    text, has_text, set_text: str text data property
    urls, has_urls, set_urls: list(str) urls property

    local_paths: list(str) local filesystem paths data

    instance, has_instance, instance_type, set_instance: python object data

"""

# Import the toolkit specific version.
from pyface.toolkit import toolkit_object

# WIP: API might change without prior notification
PyMimeData = toolkit_object('mimedata:PyMimeData')
