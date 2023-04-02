# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!


from contextlib import contextmanager
from io import BytesIO
import logging
from pickle import dumps, load, loads

import wx

from traits.api import provides
from pyface.i_clipboard import IClipboard, BaseClipboard


logger = logging.getLogger(__name__)

# Data formats
PythonObjectFormat = wx.DataFormat("PythonObject")
TextFormat = wx.DataFormat(wx.DF_TEXT)
FileFormat = wx.DataFormat(wx.DF_FILENAME)

# Shortcuts
cb = wx.TheClipboard


@contextmanager
def _ensure_clipboard():
    """ Ensure use of X11 clipboard rather than primary selection on X11.

    X11 allows pasting from either the clipboard or the primary selection.
    This context manager ensures that the clipboard is always used for Pyface,
    no matter what the wider application state is currently using.

    On non-X11 platforms this does nothing.
    """
    using_primary = cb.IsUsingPrimarySelection()
    if using_primary:
        cb.UsePrimarySelection(False)
        try:
            yield
        finally:
            cb.UsePrimarySelection(True)
    else:
        yield


@contextmanager
def _close_clipboard(flush=False):
    """ Ensures clipboard is closed and (optionally) flushed.

    Parameters
    ----------
    flush : bool
        Whether or not to flush the clipboard.  Should be true when setting
        data to the clipboard.
    """
    try:
        yield
    finally:
        cb.Close()
        if flush:
            cb.Flush()


@provides(IClipboard)
class Clipboard(BaseClipboard):
    """ WxPython implementation of the IClipboard interface.

    Python object data is transmitted as bytes consisting of the pickled class
    object followed by the corresponding pickled instance object.  This means
    that copy/paste of Python objects may not work unless compatible Python
    libraries are available at the pasting location.
    """

    # ---------------------------------------------------------------------------
    #  'data' property methods:
    # ---------------------------------------------------------------------------

    def _get_has_data(self):
        result = False
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard():
                    result = (
                        cb.IsSupported(TextFormat)
                        or cb.IsSupported(FileFormat)
                        or cb.IsSupported(PythonObjectFormat)
                    )
        return result

    # ---------------------------------------------------------------------------
    #  'object_data' property methods:
    # ---------------------------------------------------------------------------

    def _get_object_data(self):
        result = None
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard():
                    if cb.IsSupported(PythonObjectFormat):
                        cdo = wx.CustomDataObject(PythonObjectFormat)
                        if cb.GetData(cdo):
                            file = BytesIO(cdo.GetData())
                            _ = load(file)
                            result = load(file)
        return result

    def _set_object_data(self, data):
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard(flush=True):
                    cdo = wx.CustomDataObject(PythonObjectFormat)
                    cdo.SetData(dumps(data.__class__) + dumps(data))
                    # fixme: There seem to be cases where the '-1' value creates
                    # pickles that can't be unpickled (e.g. some TraitDictObject's)
                    # cdo.SetData(dumps(data, -1))
                    cb.SetData(cdo)

    def _get_has_object_data(self):
        return self._has_this_data(PythonObjectFormat)

    def _get_object_type(self):
        result = ""
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard():
                    if cb.IsSupported(PythonObjectFormat):
                        cdo = wx.CustomDataObject(PythonObjectFormat)
                        if cb.GetData(cdo):
                            try:
                                # We may not be able to load the required class:
                                result = loads(cdo.GetData())
                            except Exception:
                                logger.exception("Cannot load data from clipboard.")
        return result

    # ---------------------------------------------------------------------------
    #  'text_data' property methods:
    # ---------------------------------------------------------------------------

    def _get_text_data(self):
        result = ""
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard():
                    if cb.IsSupported(TextFormat):
                        tdo = wx.TextDataObject()
                        if cb.GetData(tdo):
                            result = tdo.GetText()
            return result

    def _set_text_data(self, data):
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard(flush=True):
                    cb.SetData(wx.TextDataObject(str(data)))

    def _get_has_text_data(self):
        return self._has_this_data(TextFormat)

    # ---------------------------------------------------------------------------
    #  'file_data' property methods:
    # ---------------------------------------------------------------------------

    def _get_file_data(self):
        with _ensure_clipboard():
            result = []
            if cb.Open():
                with _close_clipboard():
                    if cb.IsSupported(FileFormat):
                        tfo = wx.FileDataObject()
                        if cb.GetData(tfo):
                            result = tfo.GetFilenames()
            return result

    def _set_file_data(self, data):
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard(flush=True):
                    tfo = wx.FileDataObject()
                    if isinstance(data, str):
                        tfo.AddFile(data)
                    else:
                        for filename in data:
                            tfo.AddFile(filename)
                    cb.SetData(tfo)

    def _get_has_file_data(self):
        return self._has_this_data(FileFormat)

    # ---------------------------------------------------------------------------
    #  Private helper methods:
    # ---------------------------------------------------------------------------

    def _has_this_data(self, format):
        result = False
        with _ensure_clipboard():
            if cb.Open():
                with _close_clipboard():
                    result = cb.IsSupported(format)

        return result
