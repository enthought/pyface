#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------

__import__('pkg_resources').declare_namespace(__name__)


#-------------------------------------------------------------------------------
#  Define the reference to the exported Toolkit object:
#-------------------------------------------------------------------------------

import toolkit

# Reference to the Toolkit object for wxPython.
toolkit = toolkit.Toolkit_wx()
