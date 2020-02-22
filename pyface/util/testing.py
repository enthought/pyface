# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
from functools import wraps


def has_traitsui():
    """ Is traitsui installed? """
    try:
        import traitsui
    except ImportError:
        return False
    return True


def skip_if_no_traitsui(test):
    """ Decorator that skips test if traitsui not available """

    @wraps(test)
    def new_test(self):
        if has_traitsui():
            test(self)
        else:
            self.skipTest("Can't import traitsui.")

    return new_test
