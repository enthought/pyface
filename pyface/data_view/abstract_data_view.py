from traits.api import ABCHasStrictTraits, Instance, List, Tuple

from pyface.data_view.abstract_data_model import AbstractDataModel


class AbstractDataView(ABCHasStrictTraits):

    model = Instance(AbstractDataModel)

    selection = List(Tuple)

    def get_


