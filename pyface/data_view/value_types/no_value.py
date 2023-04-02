# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.data_view.abstract_value_type import AbstractValueType


class NoValue(AbstractValueType):
    """ A ValueType that has no data in any channel. """

    def has_editor_value(self, model, row, column):
        return False

    def has_text(self, model, row, column):
        return False

    def has_image(self, model, row, column):
        return False

    def has_tooltip(self, model, row, column):
        return False


#: Standard instance of the NoValue class, since it has no state.
no_value = NoValue()
