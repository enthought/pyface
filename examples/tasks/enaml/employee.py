#------------------------------------------------------------------------------
#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import datetime

from traits.api import HasTraits, Str, Int, Instance, Tuple, Date, Property


class Person(HasTraits):
    """ A simple class representing a person object.

    """
    # The last name of the person as a string
    last_name = Str

    # The first name of the person as a string
    first_name = Str

    # The date of birth of the person
    dob = Date(datetime.date(1970, 1, 1))

    # The age of the person computed from their dob
    age = Property(Int, depends_on='dob')

    # This method is called when the age of the person needs to
    # be computed
    def _get_age(self):
        today = datetime.date.today()
        dob = self.dob
        age = today.year - dob.year
        birthday_this_year = dob.replace(year=today.year)
        if today < birthday_this_year:
            age -= 1
        return age


class Employer(Person):
    """ An employer is a person who runs a company.

    """
    # The name of the company
    company_name = Str


class Employee(Person):
    """ An employee is person with a boss and a phone number.

    """
    # The employee's boss
    boss = Instance(Employer)

    # The employee's phone number as a tuple of 3 ints
    phone = Tuple(Int, Int, Int)

    # This method is called automatically by traits to get the
    # default value for the phone number.
    def _phone_default(self):
        return (555, 555, 5555)

    # This method will be called automatically by traits when the 
    # employee's phone number changes
    def _phone_changed(self, val):
        print 'received new phone number for %s: %s' % (self.first_name, val)


if __name__ == '__main__':
    # Create an employee with a boss
    boss_john = Employer(first_name='John', last_name='Paw', 
                         company_name="Packrat's Cats")
    employee_mary = Employee(first_name='Mary', last_name='Sue', 
                             boss=boss_john)

    # Import our Enaml EmployeeView
    import enaml
    with enaml.imports():
        from employee_view import EmployeeView
    
    # Create a view and show it.
    view = EmployeeView(employee=employee_mary)
    #view.show()

