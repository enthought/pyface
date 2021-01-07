# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
import contextlib
from functools import wraps
import operator
import re
from unittest import (
    mock,
    TestSuite,
)

from packaging.version import Version

from traits import __version__ as TRAITS_VERSION


def filter_tests(test_suite, exclusion_pattern):
    filtered_test_suite = TestSuite()
    for item in test_suite:
        if isinstance(item, TestSuite):
            filtered = filter_tests(item, exclusion_pattern)
            filtered_test_suite.addTest(filtered)
        else:
            match = re.search(exclusion_pattern, item.id())
            if match is not None:
                skip_msg = "Test excluded via pattern '{}'".format(
                    exclusion_pattern
                )
                setattr(item, 'setUp', lambda: item.skipTest(skip_msg))
            filtered_test_suite.addTest(item)
    return filtered_test_suite


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


def is_traits_version_ge(version):
    """ Return true if the traits version is greater than or equal to the
    required value.

    Parameters
    ----------
    version : str
        Version to be parsed. e.g. "6.0"
    """
    traits_version = Version(TRAITS_VERSION)
    given_version = Version(version)
    return traits_version >= given_version
