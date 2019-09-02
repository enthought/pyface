# Copyright (c) 2019, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

""" Toolkit-specific utilities. """

# Import the toolkit specific version.
from __future__ import absolute_import

from .toolkit import toolkit_object


# ----------------------------------------------------------------------------
# Toolkit utility functions
# ----------------------------------------------------------------------------

#: Schedule destruction of a toolkit control at a future point.
destroy_later = toolkit_object('toolkit_utils:destroy_later')

#: Checks if a toolkit control has had its underlying object deleted.
is_destroyed = toolkit_object('toolkit_utils:is_destroyed')
