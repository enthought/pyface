# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

# Enthought library imports.
from pyface.tasks.api import EnamlDockPane, EnamlTaskPane
import traits_enaml


class DummyDockPane(EnamlDockPane):
    id = "example.dummy_dock_pane"
    name = "Dummy Dock"

    def create_component(self):
        with traits_enaml.imports():
            from empty_form import EmptyForm
        return EmptyForm()


class DummyTaskPane(EnamlTaskPane):

    # TaskPane interface ---------------------------------------------------

    id = "example.dummy_task_pane"
    name = "Dummy Task"

    # ------------------------------------------------------------------------
    # 'ITaskPane' interface.
    # ------------------------------------------------------------------------

    def create_component(self):
        with traits_enaml.imports():
            from employee_view import EmployeeView
        from employee import Employer, Employee

        boss_john = Employer(
            first_name="John", last_name="Paw", company_name="Packrat's Cats"
        )
        employee_mary = Employee(
            first_name="Mary", last_name="Sue", boss=boss_john
        )

        view = EmployeeView(employee=employee_mary)
        return view
