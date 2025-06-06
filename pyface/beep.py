# (C) Copyright 2005-2025 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
# Copyright 2012 Philip Chimento

"""Sound the system bell."""

# Import the toolkit-specific version


from .toolkit import toolkit_object

beep = toolkit_object("beep:beep")
