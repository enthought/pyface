===================
Pyface Applications
===================

.. py:currentmodule:: pyface.application

Pyface provides a collection of classes suitable for representing an
application.  Although the classes are principally designed to work with
GUI-based applications, the base class :py:class:`Application` class does not
and so can be used as the basis for command-line or server applications with
a shared codebase with a GUI application.

Additionally, the application classes are designed to be forward-compatible
with Envisage application classes so applications developed using this
framework can easily be refactored to take advantage of the Envisage's plug-in
extensibility if that should be required.

Application Interface
=====================

The core of the :py:class:`Application` class' API are three methods:
:py:meth:`Application.run`, :py:meth:`Application.start`, and
:py:meth:`Application.stop`.  The :py:meth:`Application.run` method is the
entry-point of the application, and performs the following steps:

1. calls the :py:meth:`Application.start` method to initialize the
   application's state.

2. if the start is successful, calls an internal :py:meth:`Application._run`
   method which does the actual work (such as running the GUI event loop).

3. when the :py:meth:`Application._run` method returns, calls
   :py:meth:`Application.stop` to release any resources used by the application
   and de-initialize as needed.

Subclasses of the base :py:class:`Application` class will likely override all
three of these methods, but :py:class:`pyface.gui_application.GUIApplication`
subclasses may be able to avoid  having to touch them, depending on what
addition resources they need to access.

In addition to these three methods, there is an :py:meth:`Application.exit`
method that can be called by code that wants to halt the application at that
point.  For the base class this simply raises an :py:class:``ApplicationExit``
exception, but for event loop based classes it may instead call appropriate
toolkit code to close open windows and stop the application event loop.

During this life-cycle, the application will emit various Traits events
indicating the state that it is currently in.  The sequence of events is
normally :py:attr:`Application.starting`, :py:attr:`Application.started`
:py:attr:`Application.application_initialized`,
:py:attr:`Application.stopping`, and :py:attr:`Application.stopped`

In addition to the core methods and events, the :py:class:`Application` class
has some traits for metadata about the application, primarily the
human-readable application name and a unique application id.  The application
also has traits holding platform-dependent "home" and "user" directory paths,
which by default are provided by :py:mod:`traits.etsconfig` which has sane
defaults.

Application Example
-------------------

A simple command-line application might look something like this::

    import argparse
    from pyface.application import Application
    from traits.api import Str

    class HelloApplication(Application):
        """ Simple application subclass that greets a location. """

        #: The location being greeted.
        location = Str("world")

        def _run(self):
            super(HelloApplication, self)._run()
            print("Hello "+self.location)

    def main():
        app = HelloApplication()

        with app.logging(), app.excepthook():
            parser = argparse.ArgumentParser(description=app.__doc__)
            parser.add_argument('location', nargs='?', default=app.location,
                                help="the location to greet")
            parser.parse_args(namespace=app)

            app.run()

    if __name__ == '__main__':
        main()


GUIApplication Interface
========================

.. py:currentmodule:: pyface.gui_application

The :py:class:`GUIApplication` subclass is the base class to use for
Pyface-based GUI applications. This class invokes the Pyface toolkit's event
loop in the :py:meth:`GUIApplication._run` method, and stops it in the
:py:meth:`GUIApplication._exit` method.

The class has code that tracks application windows through their lifecycle.
The application has a list :py:attr:`GUIApplication.windows` of all known
windows.  Windows can be added to the list with the
:py:meth:`GUIApplication.add_window` method which also handles sizing,
decoration and opening the window.  Windows are automatically removed from the
list when they are closed.  In addition the class has a
:py:meth:`GUIApplication.create_window` method which by default calls the
:py:attr:`GUIApplication.window_factory` attribute and then calls
:py:meth:`GUIApplication.add_window`.

The :py:meth:`GUIApplication.start` method of the class must ensure that there
is at least one open window by the point that the event loop starts,
particularly with the WxPython backend.  The default
:py:meth:`GUIApplication.start` method calls
:py:meth:`GUIApplication._create_windows` to perform the initial set-up of open
windows.  The default behaviour is to call the :py:meth:`GUIApplication.create_windows`

In most cases to use the base application class, you will want to:

* create a subclass of :py:class:`pyface.application_window.ApplicationWindow`
  that at least overrides the
  :py:meth:`pyface.application_window.ApplicationWindow._create_contents`
  method to create the desired user interface.
* create a subclass of :py:class:`pyface.application_window.ApplicationWindow`
  that uses this new window class.  The application may override the
  :py:meth:`GUIApplication.create_window` method to perform additional
  application-specific customization of the windows it creates, eg. to add
  application-level menu items.

GUIApplication Example
----------------------

The following example shows how to build a simple but functional
:py:class:`GUIApplication` which provides an interactive Python shell.  The
application has two parts: a
:py:class:`pyface.application_window.ApplicationWindow` subclass which is
responsible for creating the Python shell widget, and a
:py:class:`GUIApplication` subclass which is responsible for creating the
windows and populating the menu bar.

The application window subclass looks like this::

    from pyface.api import ApplicationWindow, PythonShell
    from traits.api import Instance

    class PythonShellWindow(ApplicationWindow):
        """ An application window that displays a simple Python shell. """

        #: The title of the window.
        title = "Python Shell"

        #: The Python shell widget to use.
        shell = Instance('pyface.i_python_shell.IPythonShell')

        def _create_contents(self, parent):
            """ Create the shell widget. """
            self.shell = PythonShell(parent)
            return self.shell.control

While the GUI application window subclass looks like this::

    from pyface.api import GUIApplication
    from pyface.action.api import (
        AboutAction, CloseWindowAction, CreateWindowAction, ExitAction, Group,
        MenuBarManager, MenuManager
    )
    from python_shell_window import PythonShellWindow

    class PythonShellApplication(GUIApplication):
        """ A GUI Application which gives an interactive Python shell. """

        #: The name of the application.
        name = 'Python Shell'

        #: The window factory to use.
        window_factory = PythonShellWindow

        def create_window(self):
            """ Create the window, populating the menu bar. """
            window = self.window_factory()
            window.menu_bar_manager = self.create_menu_bar_manager(window)
            self.add_window(window)
            return window

        def create_menu_bar_manager(self, window):
            """ Create a menu bar manager for the PythonShellWindow """
            menu_bar_manager = MenuBarManager(
                MenuManager(
                    Group(CreateWindowAction(application=self)),
                    Group(
                        CloseWindowAction(window=window),
                        ExitAction(application=self),
                    ),
                    name='&File',
                ),
                MenuManager(
                    AboutAction(application=self),
                    name='&Help',
                )
            )
            return menu_bar_manager

    def main():
        app = PythonShellApplication()
        with app.logging(), app.excepthook():
            app.run()

    if __name__ == '__main__':
        main()

A more complete version of this can be found in the Pyface examples.

TasksApplication Interface
==========================

.. py:currentmodule:: pyface.tasks.tasks_application
