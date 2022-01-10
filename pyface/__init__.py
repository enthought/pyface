# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Reusable MVC-based components for Traits-based applications.
    Part of the TraitsUI project of the Enthought Tool Suite.
"""

try:
    from pyface._version import full_version as __version__
except ImportError:
    __version__ = "not-built"


__requires__ = [
    'importlib-metadata>=3.6.0; python_version<"3.8"',
    'importlib-resources>=1.1.0; python_version<"3.9"',
    "traits>=6.2",
]
__extras_require__ = {
    "wx": ["wxpython>=4", "numpy"],
    "pyqt": ["pyqt>=4.10", "pygments"],
    "pyqt5": ["pyqt5", "pygments"],
    "pyqt6": ["pyqt6", "pygments"],
    "pyside2": ["pyside2", "shiboken2", "pygments"],
    "pyside6": ["pyside6", "pygments"],
    "pillow": ["pillow"],
    "test": ["packaging"],
}


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
