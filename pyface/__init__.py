# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
Reusable components for Traits-based applications.
Part of the Enthought Tool Suite.
"""


# ============================= Test Loader ==================================

def load_tests(loader, standard_tests, pattern):
    """ Custom test loading function that enables test filtering using regex
    exclusion pattern.

    Parameters
    ----------
    loader : unittest.TestLoader
        The instance of test loader
    standard_tests : unittest.TestSuite
        Tests that would be loaded by default from this module (no tests)
    pattern : str
        An inclusion pattern used to match test files (test*.py default)

    Returns
    -------
    filtered_package_tests : unittest.TestSuite
        TestSuite representing all package tests that did not match specified
        exclusion pattern.
    """
    from os import environ
    from os.path import dirname
    from pyface.util.testing import filter_tests
    from unittest import TestSuite

    # Make sure the right toolkit is up and running before importing tests
    from pyface.toolkit import toolkit_object  # noqa: F401

    this_dir = dirname(__file__)
    package_tests = loader.discover(start_dir=this_dir, pattern=pattern)

    # List of regular expression for filtering test using the test id.
    exclusion_patterns = []

    # Environment variable for skipping more tests.
    # e.g. etstool.py in the source tree root sets this to skip packages for
    # specific toolkit
    additional_exclude = environ.get("EXCLUDE_TESTS", None)
    if additional_exclude is not None:
        exclusion_patterns.append(additional_exclude)

    filtered_package_tests = TestSuite()
    for test_suite in package_tests:
        for exclusion_pattern in exclusion_patterns:
            test_suite = filter_tests(test_suite, exclusion_pattern)
        filtered_package_tests.addTest(test_suite)

    return filtered_package_tests
