# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

# Note: The MDIApplicationWindow is currently wx-specific

# Import the toolkit specific version.
from __future__ import absolute_import

from .toolkit import toolkit_object

MDIApplicationWindow = toolkit_object(
    "mdi_application_window:MDIApplicationWindow"
)
