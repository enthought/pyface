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

""" The interface for manipulating the toolkit clipboard.
"""

# Import the toolkit specific version
from __future__ import absolute_import

from .toolkit import toolkit_object
Clipboard = toolkit_object('clipboard:Clipboard')

# Create a singleton clipboard object for convenience
clipboard = Clipboard()
