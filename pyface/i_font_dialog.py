# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The interface for a dialog that allows the user to select a color. """

from pyface.ui_traits import PyfaceFont
from pyface.i_dialog import IDialog


class IFontDialog(IDialog):
    """ The interface for a dialog that allows the user to choose a font.
    """

    # 'IFontDialog' interface ---------------------------------------------#

    #: The font in the dialog.
    font = PyfaceFont()
