# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
from functools import wraps
import re
from unittest import TestSuite

try:
    from importlib.metadata import version
except:
    from importlib_metadata import version

from packaging.version import Version


TRAITS_VERSION = version("traits")


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
    """ Is traitsui installed and sufficiently recent? """
    try:
        import traitsui  # noqa: F401
    except ImportError:
        return False
    from pyface.toolkit import toolkit
    if toolkit.toolkit.startswith("qt"):
        from pyface.qt import is_qt6
        if is_qt6:
            return Version(traitsui.__version__) >= Version("7.4")
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
