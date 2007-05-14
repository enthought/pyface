#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
#
# This software is provided without warranty under the terms of the GPL v2
# license.
#------------------------------------------------------------------------------

__import__('pkg_resources').declare_namespace(__name__)


#-------------------------------------------------------------------------------
#  Define the reference to the exported Toolkit object:
#-------------------------------------------------------------------------------

import toolkit

# Reference to the Toolkit object for PyQt v4.
toolkit = toolkit.Toolkit_qt4()
