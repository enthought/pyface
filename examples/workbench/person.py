""" A simple example of some object model. """


from traits.api import HasTraits, Int, Str


class Person(HasTraits):
    """ A simple example of some object model! """

    # Age in years.
    age = Int()

    # Name.
    name = Str()

    # ------------------------------------------------------------------------
    # 'object' interface.
    # ------------------------------------------------------------------------

    def __str__(self):
        """ Return an informal string representation of the object. """

        return self.name
