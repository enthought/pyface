#------------------------------------------------------------------------------
# Copyright (c) 2008, Enthought, Inc.
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
""" The implementation of an IPython shell. """

from __future__ import absolute_import

# Import the toolkit specific version.
try:
    import IPython.frontend
except ImportError:
    raise ImportError('''
________________________________________________________________________________
Could not load the Wx frontend for ipython.
You need to have ipython >= 0.9 installed to use the ipython widget.''')


from .toolkit import toolkit_object
IPythonWidget= toolkit_object('ipython_widget:IPythonWidget')
