# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from traits.api import Str

from pyface.data_view.abstract_value_type import AbstractValueType


class ConstantValue(AbstractValueType):
    """ A value type that does not depend on the underlying data model.

    This value type is not editable, but the other data channels it
    provides can be modified by changing the appropriate trait on the
    value type.
    """

    #: The text value to display.
    text = Str(update=True)

    def has_editor_value(self, model, row, column):
        return False

    def get_text(self, model, row, column):
        return self.text
