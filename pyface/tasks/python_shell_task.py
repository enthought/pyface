"""
Module defining a simple Python shell task.

This task provides a view with a simple Python shell.  This shouldn't be
confused with a more full-featured shell, such as those provided by IPython.
"""

# Std lib imports
import logging

# Enthought library imports.
from traits.api import Str, List, Dict, Instance, Property
from pyface.api import PythonShell
from pyface.tasks.task import Task
from pyface.task_pane import TaskPane

# set up logging
logger = logging.getLogger()


class PythonShellPane(TaskPane):
    """ A Tasks Pane containing a Pyface PythonShell
    """
    id = 'pyface.tasks.python_shell_pane'
    name = 'Python Shell'
    
    editor = Instance(PythonShell)
    
    bindings = List(Dict)
    commands = List(Str)
    
    def create(self, parent):
        logger.debug('PythonShellPane: creating python shell pane')
        self.editor = PythonShell(parent)
        self.control = self.editor.control
        
        # bind namespace
        logger.debug('PythonShellPane: binding variables')
        for binding in self.bindings:
            for name, value in binding.items():
                self.editor.bind(name, value)
        
        # execute commands
        logger.debug('PythonShellPane: executing startup commands')
        for command in self.commands:
            self.editor.execute_command(command)
               
        logger.debug('PythonShellPane: created')
    
    def destroy(self):
        logger.debug('PythonShellPane: destroying python shell pane')
        self.editor.destroy()
        self.control = self.editor = None
        logger.debug('PythonShellPane: destroyed')


class PythonShellTask(Task):
    """
    A task which provides a simple Python Shell to the user.
    """
    
    # Task Interface
    
    id = 'pyface.tasks.python_shell_task'
    name = "Python Shell"
    
    # The list of bindings for the shell
    bindings = List(Dict)
    
    # The list of commands to run on shell startup
    commands = List(Str)
    
    # Task Interface
    
    def create_central_pane(self):
        """ Create a view pane with a Python shell
        """
        logger.debug("Creating Python shell pane in central pane")
        pane = PythonShellPane(bindings=self.bindings, commands=self.commands)
        return pane
