# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The implementation of an IPython shell. """


# Import the toolkit specific version.
try:
    import IPython.frontend
except ImportError:
    raise ImportError(
        """
________________________________________________________________________________
Could not load the Wx frontend for ipython.
You need to have ipython >= 0.9 installed to use the ipython widget."""
    )


from .toolkit import toolkit_object

IPythonWidget = toolkit_object("ipython_widget:IPythonWidget")
