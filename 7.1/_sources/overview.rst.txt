.. _overview:

========
Overview
========

Pyface Concepts
===============

.. py:currentmodule:: pyface

The basic purpose of Pyface is to provide an abstraction layer between the
interface exposed to the users of the library and the actual implementation
in terms of the underlying GUI library.  To achieve this, Pyface provides
three types of object:

Interfaces
    Interface classes express the public interface for Pyface widgets.  They
    use `Trait's Interfaces <http://docs.enthought.com/traits/traits_user_manual/advanced.html#interfaces>`_
    to express this.  Interface objects are not meant to be instantiated, but
    should be used to express the types of objects that you expect in a
    toolkit-independent manner.

Mixins
    Mixin classes provide concrete implementations of certain functionality
    for a widget that are not toolkit-dependent, or can be provided purely
    using other parts of the abstract interface.  Concrete implementations
    can choose to inherit from the mixin class to use that common
    functionality.

Toolkit Implementations
    Each toolkit can provide classes that are full implementations of the
    abstract Interfaces using the widgets and other facilities provided by the
    toolkit.

In addition there is a class heirarchy othogonal to this specifying the
relationship between different types of widgets. A "dialog" for example, is a
subclass of "window", which is in turn a subclass of "widget".  This heirarchy
roughly mirrors the typical widget class system of a GUI library, and so
presents a general framework that can be abstracted between different backends.

For example, a file dialog is specified using the :py:class:`.IFileDialog`
interface, which in turn inherits from :py:class:`.IDialog`,
:py:class:`.IWindow`, and :py:class:`.IWidget`, and the full usable interface
is the combination of these.  The :py:class:`.MFileDialog` class provides some
mix-in capabilities around the expression of filters for file types.  And then
there are two concrete implementations, :py:class:`pyface.ui.wx.file_dialog.FileDialog`
for wxPython and :py:class:`pyface.ui.qt4.file_dialog.FileDialog` for the Qt
backends.  These toolkit classes in turn inherit from the appropriate toolkit's
:py:class:`Dialog`, :py:class:`Window`, and :py:class:`Widget` classes, as well
as the :py:class:`.MFileDialog` mixin.

Finally, the toolkit selected for use determines which backend class is
actually used when a program is run, allowing a developer to write code like
the following to generate a platform-independent file dialog::

    from pyface.api import FileDialog, OK

    def open_python_file():
        """ Ask the user for a Python file to open """
        dialog = FileDialog(action='open', wildcard=FileDialog.WILDCARD_PY)
        result = dialog.open()
        if result == OK:
            return dialog.path
        else:
            return None

There is a lot more to the library than just this, of course, but with this
framework in mind you can understand how Pyface is intended to be used.


Building A Pyface Application
=============================

For a minimal Pyface application, you need to do two things: create a subclass
of :py:class:`.ApplicationWindow` containing your UI,
and use the :py:class:`pyface.gui.GUI` instance to start your application's
mainloop.

This example shows how to create an application window containing a simple text
label::

    from pyface.api import ApplicationWindow, HeadingText

    class MainWindow(ApplicationWindow):
        """ The main application window. """

        # The window title.
        title = 'Hello World'

        def _create_contents(self, parent):
            """ Create the editor. """

            self._label = HeadingText(parent, text="Hello World")

            return self._label.control

The :py:class:`.IApplicationWindow` interface also allows you to provide
methods for creating menus, toolbars, and so forth.  In this example we have
used a generic cross-toolkit label widget for our content, but if we are
willing to forgo cross-platform compatibility we could create toolkit-specific
widgets instead.

Having defined your main window class, you then need to create an instance of
it, open it, and start the event loop.  We do this in a ``main()`` function
for our application::

    from pyface.api import GUI

    def main():
        # Create the GUI.
        gui = GUI()

        # Create and open the main window.
        window = MainWindow()
        window.open()

        # Start the GUI event loop!
        gui.start_event_loop()


    # Application entry point.
    if __name__ == '__main__':
        main()

Actions
=======

.. py:currentmodule:: pyface.action

An immediate desire when building a traditional GUI application is to add
menus and toolbars to allow basic user interaction via the mouse or keyboard
shortcuts.  Pyface provides these via :py:class:`~.action.Action` objects.

Actions provide the information needed to display a menu or toolbar item and
such as the title text, accelerator keys, icon and whether the action has
"radio" or "toggle" behaviour.  In addition the action needs to supply a
function to perform when the user activates it.  This is usually done by
either supplying a callable for the :py:attr:`~.action.Action.on_perform` trait of the
:py:class:`~.action.Action` or by subclassing and overriding the :py:meth:`~.action.Action.perform`
method.

The :py:attr:`~.action.Action.on_perform` is a callable that should expect no parameters to
be passed to it, so it should have all the context it needs to do what it
needs.  At its simplest, the action might look something like this::

    from pyface.action.api import Action

    def hello_world():
        print 'Hello world!'

    hello_action = Action(
        name="Hello",
        tooltip="Say hello",
        accelerator="Ctrl+Shift+H",
        on_perform=hello_world,
    )

The equivalent written as a subclass of :py:class:`~.action.Action` would look like
this::

    from pyface.action.api import Action

    class HelloAction(Action):

        #: The action's name (displayed on menus/tool bar tools etc).
        name = "Hello"

        #: Keyboard accelerator.
        accelerator = "Ctrl+Shift+H"

        #: A short description of the action used for tooltip text etc.
        tooltip = "Say hello"

        def perform(self, event=None):
            print 'Hello world!'

Because actions usually require some context, the most common use will be to
supply a class method as the :py:attr:`~.action.Action.on_perform` callable.  And for toolbar
actions, you usually want to supply an :py:attr:`~.action.Action.image` trait as well.

Actions can be organized hierarchically into groups within menus and toolbars,
and a menubar can contain multiple menus.  The following example shows how to
define a very simple Python editor application with menus::

    class MainWindow(ApplicationWindow):
        """ The main application window. """

        def __init__(self, **traits):
            """ Creates a new application window. """

            # Base class constructor.
            super(MainWindow, self).__init__(**traits)

            # Add a menu bar.
            self.menu_bar_manager = MenuBarManager(
                MenuManager(
                    Group(
                        Action(
                            name='&Open...',
                            accelerator='Ctrl+O',
                            on_perform=self.open_file
                        ),
                        Action(
                            name='&Save',
                            accelerator='Ctrl+S',
                            on_perform=self.save_file
                        ),
                        id='document_group',
                    ),
                    Action(
                        name='&Close',
                        accelerator='Ctrl+W',
                        on_perform=self.close
                    ),
                    name='&File')
            )

        def open_file(self):
            """ Open a new file. """

            if self.control:
                dlg = FileDialog(parent=self.control, wildcard="*.py")

                if dlg.open() == OK:
                    self._editor.path = dlg.path

        def save_file(self):
            """ Save the file. """

            if self.control:
                try:
                    self._editor.save()
                except IOError:
                    # If you are trying to save to a file that doesn't exist,
                    # open up a FileDialog with a 'save as' action.
                    dlg = FileDialog(
                        parent=self.control,
                        action='save as',
                        wildcard="*.py")
                    if dlg.open() == OK:
                        self._editor.save(dlg.path)

        def _create_contents(self, parent):
            """ Create the editor. """

            self._editor = PythonEditor(parent)

            return self._editor.control

Toolbars
--------

Toolbars work in a similar way to menus, each toolbar having a collection of
groups of actions.  However in addition to the options available to a menu
item, a toolbar item can have an :py:class:`~.action.Action` that provides a widget
to embed in the toolbar.  At its simplest this is done by specifying the
:py:attr:`~.action.Action.style` to be ``"widget"`` and then providing a
:py:attr:`~.action.Action.control_factory` callable that returns a toolkit object.

There are two utility subclasses provided to handle common use cases.  The
:py:class:`~.field_action.FieldAction` class takes a
:py:class:`~pyface.fields.i_field.IField` class and a dictionary of parameters
that specify the behaviour, and use this as the factory to create the
embedded widget.  :py:class:`~.field_action.FieldAction` also overrides the
:py:attr:`~.field_action.FieldAction.perform` method to pass the new value of the field
to the :py:class:`~.field_action.FieldAction.on_perform` method.

The second is the :py:class:`~.traitsui_widget_action.TraitsUIWidgetAction`
class which embeds an arbitrary TraitsUI in the toolbar.


Application Frameworks
======================

Pyface provides two application frameworks that help in building complex,
composable interfaces for applications.  The first is Workbench, which is an
older framework; the second is Tasks, which is newer and more flexible than
Workbench.  The Tasks framework is under active support, while Workbench is a
legacy codebase.

For new projects, it's recommended that developers should use Tasks if they
need such an application framework.

Both these frameworks are designed to be extensible using Envisage plugins,
and are currently documented as part of the Envisage project's documentation.

* `Workbench <http://docs.enthought.com/envisage/envisage_core_documentation/workbench.html>`_

* `Tasks <http://docs.enthought.com/envisage/tasks_user_manual/index.html>`_

Examples of building simple applications in each framework are provided in the
Pyface examples, and the APIs are auto-documented in these documents.


Pyface and TraitsUI
===================

Pyface is generally a lower-level GUI toolkit than TraitsUI, and many users
will find that TraitsUI provides all that they need.  TraitsUI uses Pyface
for some of its functionality, and the Workbench and Tasks are designed to
easily incoprorate UIs built using TraitsUI.

It is fairly straightforward to use or embed a TraitsUI view into a Pyface
widget: the basic approach is to call :py:meth:`edit_traits` with
``kind='panel'`` from inside the :py:meth:`_create_control` method (or
equivalent, like :py:meth:`_create_contents` when embedding in a window
or dialog) of the widget, extract the toolkit control from the resulting
:py:obj:`ui` object, and return or embed that control.

For example, to embed a TraitsUI View in an :py:class:`ApplicationWindow`,
you might do something like this::

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

        # The size of the window.
        size = (320, 240)

        # The window title.
        title = 'TraitsUI Person'

        # The traits object to display
        person = Instance(Person, ())

        def _create_contents(self, parent):
            """ Create the editor. """
            self._ui = self.person.edit_traits(kind='panel', parent=parent)
            return self._ui.control

A similar approach can be used when working with Enaml, Matplotlib, or other
libraries which can produce a toolkit-specific control.
