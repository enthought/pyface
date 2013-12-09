#------------------------------------------------------------------------------
# Copyright (c) 2013, Enthought, Inc.
# All rights reserved.
#------------------------------------------------------------------------------

# Enthought library imports.
from pyface.tasks.api import EnamlDockPane, EnamlTaskPane
import traits_enaml


class DummyDockPane(EnamlDockPane):
    id = 'example.dummy_dock_pane'
    name = 'Dummy Dock'

    def create_component(self):
        with traits_enaml.imports():
            from empty_form import EmptyForm
        return EmptyForm()


class DummyTaskPane(EnamlTaskPane):

    #### TaskPane interface ###################################################

    id = 'example.dummy_task_pane'
    name = 'Dummy Task'

    ###########################################################################
    # 'ITaskPane' interface.
    ###########################################################################

    def create_component(self):
        with traits_enaml.imports():
            from employee_view import EmployeeView
        from employee import Employer, Employee

        boss_john = Employer(first_name='John', last_name='Paw',
                             company_name="Packrat's Cats")
        employee_mary = Employee(first_name='Mary', last_name='Sue',
                                 boss=boss_john)

        view = EmployeeView(employee=employee_mary)
        return view
