Undo Framework
==============

The Undo Framework is a component of the Enthought Tool Suite that provides
developers with an API that implements the standard pattern for do/undo/redo
commands.

The framework is completely configurable.  Alternate implementations of all
major components can be provided if necessary.


Framework Concepts
------------------

The following are the concepts supported by the framework.

- Command

  A command is an application defined operation that can be done (i.e.
  executed), undone (i.e. reverted) and redone (i.e. repeated).

  A command operates on some data and maintains sufficient state to allow it to
  revert or repeat a change to the data.

  Commands may be merged so that potentially long sequences of similar
  commands (e.g. to add a character to some text) can be collapsed into a
  single command (e.g. to add a word to some text).

- Macro

  A macro is a sequence of commands that is treated as a single command when
  being undone or redone.

- Command Stack

  A command is done by pushing it onto a command stack.  The last command can
  be undone and redone by calling appropriate command stack methods.  It is
  also possible to move the stack's position to any point and the command stack
  will ensure that commands are undone or redone as required.

  A command stack maintains a *clean* state which is updated as commands are
  done and undone.  It may be explicitly set, for example when the data being
  manipulated by the commands is saved to disk.

  Canned PyFace actions are provided as wrappers around command stack methods
  to implement common menu items.

- Undo Manager

  An undo manager is responsible for one or more command stacks and maintains
  a reference to the currently active stack.  It provides convenience undo and
  redo methods that operate on the currently active stack.

  An undo manager ensures that each command execution is allocated a unique
  sequence number, irrespective of which command stack it is pushed to.  Using
  this it is possible to synchronise multiple command stacks and restore them
  to a particular point in time.

  An undo manager will generate an event whenever the clean state of the active
  stack changes.  This can be used to maintain some sort of GUI status
  indicator to tell the user that their data has been modified since it was
  last saved.

Typically an application will have one undo manager and one undo stack for
each data type that can be edited.  However this is not a requirement: how the
command stack's in particular are organised and linked (with the user
manager's sequence number) can need careful thought so as not to confuse the
user - particularly in a plugin based application that may have many editors.

To support this typical usage the PyFace ``Workbench`` class has an
``undo_manager`` trait and the PyFace ``Editor`` class has a ``command_stack``
trait.  Both are lazy loaded so can be completely ignored if they are not used.


API Overview
------------

This section gives a brief overview of the various classes implemented in the
framework.  The complete API_ documentation is available as endo generated
HTML.

The example_ application demonstrates all the major features of the framework.


UndoManager
...........

The ``UndoManager`` class is the default implementation of the ``IUndoManager``
interface.

``active_stack``
    This trait is a reference to the currently active command stack and may be
    None.  Typically it is set when some sort of editor becomes active.

``active_stack_clean``
    This boolean trait reflects the clean state of the currently active
    command stack.  It is intended to support a "document modified" indicator
    in the GUI.  It is maintained by the undo manager.

``stack_updated``
    This event is fired when the index of a command stack is changed.  A
    reference to the stack is passed as an argument to the event and may not
    be the currently active stack.

``undo_name``
    This Str trait is the name of the command that can be undone, and will
    be empty if there is no such command.  It is maintained by the undo
    manager.

``redo_name``
    This Str trait is the name of the command that can be redone, and will
    be empty if there is no such command.  It is maintained by the undo
    manager.

``sequence_nr``
    This integer trait is the sequence number of the next command to be
    executed.  It is incremented immediately before a command's ``do()``
    method is called.  A particular sequence number identifies the state of
    all command stacks handled by the undo manager and allows those stacks to
    be set to the point they were at at a particular point in time.  In other
    words, the sequence number allows otherwise independent command stacks to
    be synchronised.

``undo()``
    This method calls the ``undo()`` method of the last command on the active
    command stack.

``redo()``
    This method calls the ``redo()`` method of the last undone command on the
    active command stack.


CommandStack
............

The ``CommandStack`` class is the default implementation of the
``ICommandStack`` interface.

``clean``
    This boolean traits reflects the clean state of the command stack.  Its
    value changes as commands are executed, undone and redone.  It may also be
    explicitly set to mark the current stack position as being clean (when
    data is saved to disk for example).

``undo_name``
    This Str trait is the name of the command that can be undone, and will
    be empty if there is no such command.  It is maintained by the command
    stack.

``redo_name``
    This Str trait is the name of the command that can be redone, and will
    be empty if there is no such command.  It is maintained by the command
    stack.

``undo_manager``
    This trait is a reference to the undo manager that manages the command
    stack.

``push(command)``
    This method executes the given command by calling its ``do()`` method.
    Any value returned by ``do()`` is returned by ``push()``.  If the command
    couldn't be merged with the previous one then it is saved on the command
    stack.

``undo(sequence_nr=0)``
    This method undoes the last command.  If a sequence number is given then
    all commands are undone up to an including the sequence number.

``redo(sequence_nr=0)``
    This method redoes the last command and returns any result.  If a sequence
    number is given then all commands are redone up to an including the
    sequence number and any result of the last of these is returned.

``clear()``
    This method clears the command stack, without undoing or redoing any
    commands, and leaves the stack in a clean state.  It is typically used
    when all changes to the data have been abandoned.

``begin_macro(name)``
    This method begins a macro by creating an empty command with the given
    name.  The commands passed to all subsequent calls to ``push()`` will be
    contained in the macro until the next call to ``end_macro()``.  Macros may
    be nested.  The command stack is disabled (ie. nothing can be undone or
    redone) while a macro is being created (ie. while there is an outstanding
    ``end_macro()`` call).

``end_macro()``
    This method ends the current macro.


ICommand
........

The ``ICommand`` interface defines the interface that must be implemented by
any undoable/redoable command.

``data``
    This optional trait is a reference to the data object that the command
    operates on.  It is not used by the framework itself.

``name``
    This Str trait is the name of the command as it will appear in any GUI
    element (e.g. in the text of an undo and redo menu entry).  It may include
    ``&`` to indicate a keyboard shortcut which will be automatically removed
    whenever it is inappropriate.

``__init__(*args)``
    If the command takes arguments then the command must ensure that deep
    copies should be made if appropriate.

``do()``
    This method is called by a command stack to execute the command and to
    return any result.  The command must save any state necessary for the
    ``undo()`` and ``redo()`` methods to work.  It is guaranteed that this
    will only ever be called once and that it will be called before any call
    to ``undo()`` or ``redo()``.

``undo()``
    This method is called by a command stack to undo the command.

``redo()``
    This method is called by a command stack to redo the command and to return
    any result.

``merge(other)``
    This method is called by the command stack to try and merge the ``other``
    command with this one.  True should be returned if the commands were
    merged.  If the commands are merged then ``other`` will not be placed on
    the command stack.  A subsequent undo or redo of this modified command
    must have the same effect as the two original commands.


AbstractCommand
...............

``AbstractCommand`` is an abstract base class that implements the ``ICommand``
interface.  It provides a default implementation of the ``merge()`` method.


CommandAction
.............

The ``CommandAction`` class is a sub-class of the PyFace ``Action`` class that
is used to wrap commands.

``command``
    This callable trait must be set to a factory that will return an object
    that implements ``ICommand``.  It will be called when the action is invoked
    and the object created pushed onto the command stack.

``command_stack``
    This instance trait must be set to the command stack that commands invoked
    by the action are pushed to.

``data``
    This optional trait is a reference to the data object that will be passed
    to the ``command`` factory when it is called.


UndoAction
..........

The ``UndoAction`` class is a canned PyFace action that undoes the last
command of the active command stack.


RedoAction
..........

The ``RedoAction`` class is a canned PyFace action that redoes the last
command undone of the active command stack.


.. _API: api/index.html
.. _example: https://svn.enthought.com/enthought/browser/AppTools/trunk/examples/undo/
