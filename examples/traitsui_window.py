#------------------------------------------------------------------------------
#
#  Copyright (c) 2009, Enthought, Inc.
#  All rights reserved.
#
#  This software is provided without warranty under the terms of the BSD
#  license included in enthought/LICENSE.txt and may be redistributed only
#  under the conditions described in the aforementioned license.  The license
#  is also available online at http://www.enthought.com/licenses/BSD.txt
#
#  Thanks for using Enthought open source!
#
#------------------------------------------------------------------------------
""" IPython widget example. """

# Enthought library imports.
from pyface.api import ApplicationWindow, GUI
from pyface.ipython_widget import IPythonWidget
from traits.api import Enum, HasTraits, Instance, Int, Str
from traitsui.api import View, Item


class Person(HasTraits):
    """ Model class representing a person """

    #: the name of the person
    name = Str

    #: the age of the person
    age = Int(18)

    #: the gender of the person
    gender = Enum('female', 'male')

    # a default traits view
    view = View(
        Item('name', resizable=True),
        Item('age', resizable=True),
        Item('gender', resizable=True),
        resizable=True,
    )


class MainWindow(ApplicationWindow):
    """ The main application window. """

    #### 'IWindow' interface ##################################################

    # The size of the window.
    size = (320, 240)

    # The window title.
    title = 'TraitsUI Person'

    # The traits object to display
    person = Instance(Person, ())

    ###########################################################################
    # Protected 'IApplication' interface.
    ###########################################################################

    def _create_contents(self, parent):
        """ Create the editor. """
        self._ui = self.person.edit_traits(kind='panel', parent=parent)
        return self._ui.control


# Application entry point.
if __name__ == '__main__':
    # Create the GUI.
    gui = GUI()

    # Create and open the main window.
    window = MainWindow()
    window.open()

    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #####################################################################
