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

  PyFace actions are provided as wrappers around command stack methods
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
