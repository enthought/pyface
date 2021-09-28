# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The implementation of access to system metrics (screen width and height
etc).
"""


# Import the toolkit specific version.


from .toolkit import toolkit_object

SystemMetrics = toolkit_object("system_metrics:SystemMetrics")
