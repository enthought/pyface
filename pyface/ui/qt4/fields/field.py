# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Qt-specific implementation of the text field class """


from traits.api import Any, provides

from pyface.fields.i_field import IField, MField
from pyface.ui.qt4.layout_widget import LayoutWidget


@provides(IField)
class Field(MField, LayoutWidget):
    """ The Qt-specific implementation of the field class

    This is an abstract class which is not meant to be instantiated.
    """

    #: The value held by the field.
    value = Any()
