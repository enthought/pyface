# Standard library imports.
import logging

import os

# Logger.
logger = logging.getLogger(__name__)
print __name__

requested = ""
if 'ETS_WX_AUI' in os.environ:
    requested = os.environ['ETS_WX_AUI']

aui = None
try:
    if requested.lower() == "wx":
        from wx import aui
    elif requested.lower() == "agw":
        from wx.lib.agw import aui
except ImportError:
    logger.warn('Requested AUI toolkit (ETS_WX_AUI=%s) not available', requested)

if aui is None:
    # If nothing specified, prefer the pure python implementation of AUI if
    # available
    try:
        from wx.lib.agw import aui
    except ImportError:
        try:
            from wx import aui
        except ImportError:
            aui = None
