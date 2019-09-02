# Copyright (c) 2013-19 by Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

from __future__ import absolute_import, print_function

from contextlib import contextmanager
import os
import sys


@contextmanager
def silence_output(out=None, err=None):
    """ Re-direct the stderr and stdout streams while in the block. """

    with _convert_none_to_null_handle(out) as out:
        with _convert_none_to_null_handle(err) as err:
            _old_stderr = sys.stderr
            _old_stderr.flush()

            _old_stdout = sys.stdout
            _old_stdout.flush()

            try:
                sys.stdout = out
                sys.stderr = err
                yield
            finally:
                sys.stdout = _old_stdout
                sys.stderr = _old_stderr


@contextmanager
def _convert_none_to_null_handle(stream):
    """ If 'stream' is None, provide a temporary handle to /dev/null. """

    if stream is None:
        out = open(os.devnull, 'w')
        try:
            yield out
        finally:
            out.close()
    else:
        yield stream
