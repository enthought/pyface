.. _standard_dialogs:

================
Standard Dialogs
================

In addition to being able to create custom dialogs based on the |IDialog|
interface, Pyface exposes a number of standard toolkit and OS dialogs.

About Dialog
============

.. figure:: images/about_dialog.png
   :scale: 50
   :alt: an about dialog

   An About Dialog

A dialog that displays a simple message about the application, along with a
logo and copyright information.  This is designed to be suitable to be called
from an "About" menu item.

Color Dialog
============

.. figure:: images/color_dialog.png
   :scale: 50
   :alt: a color dialog on Mac OS

   A Color Dialog on Mac OS

A dialog that takes a |Color| object and displays a standard OS color-picker
dialog with an option that allows the setting of transparency/alpha if needed.

A convenience function |get_color| opens the dialog and returns a color value.

Confirmation Dialog
===================

.. figure:: images/confirmation_dialog.png
   :scale: 50
   :alt: a confirmation dialog

   A Confirmation Dialog

A dialog that presents a message and allows the user to select a Yes/No
response, with the option to present a Cancel button as well.  The default
button, as well as the labels for the buttons can be controlled.
The result value is one of the pyface constants of |CANCEL|, |YES| or
|NO|.

A convenience function |confirm| provides a simple API for opening a dialog
and returning the result.

Directory Dialog
================

A dialog that shows the standard OS file selection dialog for directories only,
as well as whether the dialog should follow "Open" or "Save As" conventions for
selecting a directory. Other options allow specifying a default path.

Typical usage for a save dialog looks like this::

    # display a directory dialog for opening a directory
    dialog = DirectoryDialog(parent=None)
    if dialog.open() == OK:
        print(f"Open {dialog.path}")


File Dialog
===========

A dialog that shows the standard OS file selection dialog, with options to
filter by file type as well as whether the dialog should follow "Open" or
"Save As" conventions.  Other options allow specifying a default directory and
file, and wildcards for filtering file type extensions.

Typical usage for a save dialog looks like this::

    # display a file dialog for saving a Python file
    dialog = FileDialog(parent=None, action="save as", wildcard="*.py")
    if dialog.open() == OK:
        print(f"Save to {dialog.path}")


Font Dialog
===========

A dialog that takes a |Font| object and displays a standard OS font selection.
A convenience function |get_font| opens the dialog and returns a font value.


Message Dialog
==============

.. figure:: images/error_dialog.png
   :scale: 50
   :alt: an error message dialog

   An Error Message Dialog

A dialog that shows the standard OS message dialog, where the user is only
presented with the ability to confirm the message.  The dialog has a "severity"
trait which can take the values of ``"information"``, ``"warning"`` or
``"error"`` and displays an appropriate icon along with the message.

There are convenience functions |information|, |warning| and |error| that
create a dialog of the appropriate severity level.

Progress Dialog
===============

.. figure:: images/progress_dialog.png
   :scale: 50
   :alt: a progress dialog

   A Progress Dialog

This class displays a progress bar in a dialog, together with a message and
various additonal optional information, such as time estimates.  The progress
dialog is designed to integrate with long-running computations that are using
the main thread, and make an effort to keep the UI at least minimally
responsive::

    def create_thumbnails(paths, size=(128, 128)):
        progress = ProgressDialog(
            title="Creating Thumbnails...",
            max=len(paths),
        )
        progress.open()

        for i, path in enumerate(paths):
            progress.message = f"Processing: {path}"
            file, ext = os.path.splitext(path)
            with Image.open(path) as im:
                im.thumbnail(size)
                im.save(file + "_thumbnail.png")
            (cont, skip) = progress.update(i)
            if not cont or skip:
                break

        progress.update(len(paths))

It can also be used with Python's standard library |Executor| classes to take
advantage of potential parallelism::

    def create_thumbnail(path, size):
        file, ext = os.path.splitext(path)
        with Image.open(path) as im:
            im.thumbnail(size)
            im.save(file + "_thumbnail.png")
        return path

    def create_thumbnails(paths, size=(128, 128)):
        executor = ThreadPoolExecutor()
        progress = ProgressDialog(
            title="Creating Thumbnails...",
            max=len(paths),
        )
        progress.open()

        for i, path in enumerate(map(create_thumbnail, paths)):
            progress.message = f"Processing: {path}"
            (cont, skip) = progress.update(i)
            if not cont or skip:
                break

        executor.shutdown(cancel_futures=True)

        progress.update(len(paths))

This is in contrast with the situation where operations are handled using a
"fire-and-forget" process where computations are dispatched in the background,
with any opportunity for updates coming via callbacks.  Since these sorts of
jobs run in the background, a dialog (particularly a modal dialog), may not
provide the best UX.

This dialog is well-suited to situations where there are many steps to
perform, each of which takes a small amount of time.  If instead there is only
one step that can take a long time to perform, or if the total number of steps
isn't known, setting the min and max to 0 shows an indeterminate busy indicator
in the place of the bar.

The progress dialog has the option to provide a cancel button that the user
can use to stop the underlying process.

Single-Choice Dialog
====================

.. figure:: images/single_choice_dialog.png
   :scale: 50
   :alt: a single-choice dialog

   A Single-Choice Dialog

A dialog which presents a list-box with a set of choices for the user and
permits the selection of one of them, or to cancel.  There is also a
|choose_one| convenience function which takes a list of options and either the
user's selection or ``None`` if nothing is selected.


.. |CANCEL| replace:: :py:obj:`~pyface.constants.CANCEL`
.. |Color| replace:: :py:class:`~pyface.color.Color`
.. |Executor| replace:: :py:class:`~concurrent.futures.Executor`
.. |Font| replace:: :py:class:`~pyface.font.Font`
.. |IDialog| replace:: :py:class:`~pyface.i_dialog.IDialog`
.. |NO| replace:: :py:obj:`~pyface.constants.NO`
.. |OK| replace:: :py:obj:`~pyface.constants.OK`
.. |YES| replace:: :py:obj:`~pyface.constants.YES`
.. |choose_one| replace:: :py:func:`~pyface.single_choice_dialog.choose_one`
.. |confirm| replace:: :py:func:`~pyface.confirmation_dialog.confirm`
.. |error| replace:: :py:func:`~pyface.message_dialog.error`
.. |get_color| replace:: :py:func:`~pyface.color_dialog.get_color`
.. |get_font| replace:: :py:func:`~pyface.font_dialog.get_font`
.. |information| replace:: :py:func:`~pyface.message_dialog.information`
.. |open| replace:: :py:meth:`~pyface.i_dialog.IDialog.open`
.. |warning| replace:: :py:func:`~pyface.message_dialog.warning`
.. |_create_buttons| replace:: :py:meth:`~pyface.i_dialog.IDialog._create_buttons`
.. |_create_dialog_area| replace:: :py:meth:`~pyface.i_dialog.IDialog._create_dialog_area`
