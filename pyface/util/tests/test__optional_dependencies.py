# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the _optional_dependencies module """

import unittest

from pyface.util._optional_dependencies import optional_import

#: Name of the logger used for logging debug messages from optional_import
TARGET_LOGGER_NAME = "pyface"


class TestOptionalImport(unittest.TestCase):
    """ Test optional import context manager """

    def test_optional_import(self):
        # Test excusing dependency on 'some_random.path'

        with self.assertLogs(TARGET_LOGGER_NAME, level="DEBUG") as log_context:
            with optional_import("random_missing_lib", "fail to import"):
                # assume this library is not importable.
                import random_missing_lib   # noqa: F401

        log, = log_context.output
        self.assertIn("fail to import", log)

    def test_optional_import_reraise(self):
        # Test if the import error was about something else, reraise
        with self.assertRaises(ImportError):
            with optional_import("some_random_lib", ""):
                import some_random_missing_lib   # noqa: F401
