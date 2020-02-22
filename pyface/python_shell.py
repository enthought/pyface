# ------------------------------------------------------------------------------
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
# ------------------------------------------------------------------------------
""" The implementation of an interactive Python shell. """


# Import the toolkit specific version.
from __future__ import absolute_import

from .toolkit import toolkit_object

PythonShell = toolkit_object("python_shell:PythonShell")

#### EOF ######################################################################
