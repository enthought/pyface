# Copyright (c) 2017, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!

import logging

logger = logging.getLogger(__name__)
logger.warning(
    'DEPRECATED: pyface.image_list, use pyface.ui.wx.image_list instead. '
    'Will be removed in Pyface 7.')

from pyface.ui.wx.image_list import *
