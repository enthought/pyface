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
subclasses may be able to avoid having to touch them, depending on what
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
human-readable application name, a description of the application, and a
globally unique application id.  The application also has traits holding
platform-dependent "home" and "user" directory paths, which by default are
provided by :py:mod:`traits.etsconfig` which give reasonable platform-dependent
results.

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

        parser = argparse.ArgumentParser(description=app.description)
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
:py:meth:`GUIApplication.add_window` method which also handles opening the
window.  Windows are automatically removed from the list when they are closed.
In addition the class has a :py:meth:`GUIApplication.create_window` method
which by default calls the :py:attr:`GUIApplication.window_factory` attribute
and handles setting titles, icons and sizing of the created windows.  Windows
created by :py:meth:`GUIApplication.create_window` still need to be added to
the application's list of windows via :py:meth:`GUIApplication.add_window`.

The :py:meth:`GUIApplication.start` method of the class must ensure that there
is at least one open window by the point that the event loop starts,
particularly with the WxPython backend.  The default
:py:meth:`GUIApplication.start` method calls
:py:meth:`GUIApplication._create_windows` to perform the initial set-up of open
windows.  The default behaviour is to call the
:py:meth:`GUIApplication.create_windows` method and then add that window.

In most cases to use the base :py:class:`GUIApplication` class, you will want
to:

* create a subclass of :py:class:`~pyface.application_window.ApplicationWindow`
  that at least overrides the
  :py:meth:`~pyface.application_window.ApplicationWindow._create_contents`
  method to create the desired user interface.  Ideally this window should be
  able to work without needing an application, as this helps with reusability.
* create a window factory function that taskes the application and arbitrary
  other keyword arguments and creates an instance of the 
  :py:class:`~pyface.application_window.ApplicationWindow` subclass along with
  any additional application-dependent state that is required. This can
  include application-dependent menus, toolbars, etc. as well as other state
  injected by from application.

While the :py:class:`GUIApplication` class can be used without subclassing, for
complex applications it is likely that the a subclass will need to be used,
and will likely override the :py:meth:`~GUIApplication.start`,
:py:meth:`~GUIApplication.stop` and :py:meth:`~GUIApplication.create_window`
methods to perform additional application-specific customization.

GUIApplication Example
----------------------

The following example shows how to build a simple but functional
:py:class:`GUIApplication` which provides an interactive Python shell.  The
application has two parts: a
:py:class:`pyface.application_window.ApplicationWindow` subclass which is
responsible for creating the Python shell widget, and a window factory which
is responsible for creating the windows and populating the menu bar.

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

Note that we don't (and shouldn't) need the application to be available for
this class to work - it is a perfectly good stand-alone class that can
potentially be re-used in many different contexts.

While the GUI application window subclass looks like this::

    from pyface.api import GUIApplication
    from pyface.action.api import (
        AboutAction, CloseWindowAction, CreateWindowAction, ExitAction, Group,
        MenuBarManager, MenuManager
    )
    from python_shell_window import PythonShellWindow

    def create_python_shell_window(application, **kwargs):
        window = PythonShellWindow()
        window.menu_bar_manager = MenuBarManager(
            MenuManager(
                Group(CreateWindowAction(application=application)),
                Group(
                    CloseWindowAction(window=window),
                    ExitAction(application=application),
                ),
                name='&File',
            ),
            MenuManager(
                AboutAction(application=application),
                name='&Help',
            )
        )
        return window

    def main():
        app = GUIApplication(
            name="Python Shell",
            description="An example application that provides a Python shell.",
            icon='python_icon',
            logo='python_logo',
            window_factory=create_python_shell_window,
        )
        app.run()

    if __name__ == '__main__':
        main()

A more complete version of this can be found in the Pyface examples.

TasksApplication Interface
==========================

.. py:currentmodule:: pyface.tasks.tasks_application

The :py:class:`TasksApplication` class works in a similar way to the
:py:class:`~pyface.gui_application.GUIApplication` class, but instead of the
supplying a window factory, instead you provide one or more
:py:class:`TaskFactory` instances which provide information about the
different Tasks that are available for each window.

In addition the :py:class:`TasksApplication` has traits that hold extra
application-specific :py:class:`~pyface.actions.action.Action`s via the
:py:class:`~pyface.tasks.actions.schema_addition.SchemaAddition` mechanism,
and :py:class:`~pyface.tasks.dock_pane.DockPane` via factories for creating
the dock panes.

A complete :py:class:`TasksApplication` can be as simple as::

    from pyface.tasks.api import TaskFactory, TasksApplication
    from python_editor_task import PythonEditorTask

    def main():
        app = TasksApplication(
            id="example_python_editor_application",
            name="Python Editor",
            description=(
                "An example Tasks application that provides a Python editor."
            ),
            icon='python_icon',
            logo='python_logo',
            task_factories=[
                TaskFactory(
                    id='example.python_editor_task',
                    name="Python Editor",
                    factory=PythonEditorTask
                )
            ],
        )

        # invoke the mainloop
        app.run()

    if __name__ == '__main__':
        main()

A more complete version of this can be found in the Pyface examples.
