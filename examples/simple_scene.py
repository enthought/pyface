#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
# 
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
""" TVTK simple scene example. """

print "This example will not work with wxPython versions 2.8 or higher."

# Standard library imports.
import os, random, sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r'..\..\..'))

# Enthought library imports.
from enthought.pyface.api import GUI
from enthought.pyface.api import PythonShell
from enthought.pyface.api import SplitApplicationWindow
from enthought.pyface.tvtk.simple_scene import SimpleScene
from enthought.pyface.tvtk.actors import *
from enthought.traits.api import Float, Str, Instance


class MainWindow(SplitApplicationWindow):
    """ The main application window. """

    # The actors we can create.
    ACTORS = [
        arrow_actor, axes_actor, cone_actor, cube_actor, cylinder_actor,
        earth_actor, sphere_actor
    ]

    #### 'SplitApplicationWindow' interface ###################################
    
    # The ratio of the size of the left/top pane to the right/bottom pane.
    ratio = Float(0.75)

    # The direction in which the panel is split.
    direction = Str('horizontal')

    #### Private interface ####################################################

    # The `Scene` instance into which VTK renders.
    _scene = Instance(SimpleScene)

    # The `PythonShell` instance.
    _python_shell = Instance(PythonShell)

    ###########################################################################
    # Protected 'SplitApplicationWindow' interface.
    ###########################################################################

    def _create_lhs(self, parent):
        """ Creates the left hand side or top depending on the style. """

        self._scene = SimpleScene(parent)

        # Add some actors.
        for i in range(10):
            func = random.choice(self.ACTORS)
            actor = func()

            # Place the actor randomly.
            x = random.uniform(-3, 3)
            y = random.uniform(-3, 3)
            z = random.uniform(-3, 3)

            actor.position = x, y, z

            # Add the actor to the scene.
            self._scene.add_actor(actor)

        # Render it all!
        self._scene.render()
        
        return self._scene.control

    def _create_rhs(self, parent):
        """ Creates the right hand side or bottom depending on the style. """

        self._python_shell = PythonShell(parent)
        self._python_shell.bind('widget', self._scene)
        self._python_shell.bind('w', self._scene)
        
        return self._python_shell.control


# Application entry point.
if __name__ == '__main__':
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    # Create and open the main window.
    window = MainWindow(size=(600,600))
    window.open()
    
    # Start the GUI event loop!
    gui.start_event_loop()

##### EOF #####################################################################
