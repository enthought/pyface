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
# Description: <Enthought util package component>
#------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#
#  Provides a simple function for scheduling some code to run at some time in
#  the future (assumes application is wxPython based).
#
#  Written by: David C. Morrill
#
#  Date: 05/18/2005
#
#  (c) Copyright 2005 by Enthought, Inc.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#  Imports:
#-------------------------------------------------------------------------------

# Import the toolkit specific version.
from pyface.toolkit import toolkit_object
DoLaterTimer = toolkit_object('timer.do_later:DoLaterTimer')

#-------------------------------------------------------------------------------
#  Does something 50 milliseconds from now:
#-------------------------------------------------------------------------------

def do_later ( callable, *args, **kw_args ):
    """ Does something 50 milliseconds from now.
    """
    DoLaterTimer( 50, callable, args, kw_args )

#-------------------------------------------------------------------------------
#  Does something after some specified time interval:
#-------------------------------------------------------------------------------

def do_after ( interval, callable, *args, **kw_args ):
    """ Does something after some specified time interval.
    """
    DoLaterTimer( interval, callable, args, kw_args )
