# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!
""" Tests for the _optional_dependencies module """

import logging
import unittest

from pyface.util._optional_dependencies import optional_import


class TestOptionalImport(unittest.TestCase):
    """ Test optional import context manager """

    def test_optional_import(self):
        # Test excusing dependency and the logging behaviour
        logger = logging.getLogger(self.id())
        with self.assertLogs(logger, level="DEBUG") as log_context:
            with optional_import(
                    "random_missing_lib", "fail to import", logger):
                # assume this library is not importable.
                import random_missing_lib   # noqa: F401

        log, = log_context.output
        self.assertIn("fail to import", log)

    def test_optional_import_reraise(self):
        # Test if the import error was about something else, reraise
        logger = logging.getLogger(self.id())
        with self.assertRaises(ImportError):
            with optional_import("some_random_lib", "", logger):
                import some_random_missing_lib   # noqa: F401
