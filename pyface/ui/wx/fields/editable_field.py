# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" The Wx-specific implementation of the text field class """


from traits.api import provides

from pyface.fields.i_editable_field import IEditableField, MEditableField
from pyface.ui.wx.fields.field import Field


@provides(IEditableField)
class EditableField(MEditableField, Field):
    """ The Wx-specific implementation of the EditableField class

    This is an abstract class which is not meant to be instantiated.
    """
