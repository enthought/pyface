""" This file contains an implementation of the custom editor.

This is shared between two different designs. Corran will probably
implement this slightly differently, but there are no major design
concern here... unless Kit misunderstood what Corran meant (again).
"""


from traits.api import (
    Any, Bool, Event, List, Instance, HasStrictTraits, Dict, Callable, observe,
    Property, Str, Int, Enum
)


class BaseItemEditorFactory:
    """ Base class for implementing a custom item editor.

    This can be made an interface instead, but with this being a public
    library API, using a base class is more flexible. It is hard to add
    features to a published interface, but it is easier to add
    features to a published base class.
    """

    def create(self, parent, item_handle):
        """ Create the toolkit specific object as the custom editor.

        Parameters
        ----------
        parent : any
            Toolkit specific parent widget.
        item_handle : ItemHandle
            Handle for obtaining data from the data model as well as the
            row/column index this custom editor is referring to.

        Returns
        -------
        control : any
            Toolkit specific widget.
        """
        raise NotImplementedError("This method must return a widget control.")

    def commit(self, control, handle):
        """ Commit data at the end of an edit.

        If the user presses Escape to exit the edit mode, this method
        will not be called. If the user clicks outside of the editor or
        presses Tab (as long as it is not also captured by the editor), then
        this method is called to commit the data change.

        Default behaviour does nothing.

        Parameters
        ----------
        control : any
            Widget returned by ``create``.
        handle : ItemHandle
            Handle for commiting data. The commit action can be achieved by
            assigning value to ItemHandle.value.
        """
        pass

    def destroy(self, control):
        """ Implement how to dispose the control created.

        Note: This is not used in Qt4.

        If NotImplementedError is raised, the default behaviour is to
        destroy the control. Override this method to avoid the control
        being destroyed, or to do additional clean up before the control is
        destroyed.
        """
        raise NotImplementedError("No custom behaviour is implemented.")


class FileDialogItemEditorFactory(BaseItemEditorFactory, HasStrictTraits):
    """ Implementation for setting a file path from the system file dialog.

    We can probably use ``FileDialog`` from pyface, then this factory can
    write toolkit agnostic code.
    """

    # Either 'open' or 'save'
    mode = Str("open")

    def create(self, parent, item_handle):
        from pyface.qt import QtGui
        dlg = QtGui.QFileDialog(parent)
        value = item_handle.model.get_value(
            item_handle.row, item_handle.column
        )
        if value:
            dlg.selectFile(value)

        if self.mode == "open":
            dlg.setAcceptMode(dlg.AcceptOpen)
        elif self.mode == "save":
            dlg.setAcceptMode(dlg.AcceptSave)
        dlg.setModal(True)
        return dlg

    def commit(self, control, handle):
        from pyface.qt import QtGui
        if control.result() == QtGui.QDialog.Accepted:
            files = control.selectedFiles()
            if files:
                handle.set_value(files[0])
            # warn about more than one file.

    # Use default destroy implementation.


class TraitsUIItemObject(HasStrictTraits):
    """ Object to hold the value being edited so that it does not immediately
    set on the data model. This delay effect only works when the editing occurs
    directly on the value, e.g. it would not work on InstanceEditor where the
    value is an object and the edited quantities are values on the object.
    """
    value = Any()


class TraitsUIItemEditorFactory(BaseItemEditorFactory, HasStrictTraits):
    """ An implementation of a BaseItemEditorFactory that allows any TraitsUI
    editor to be used as the item editor.

    The factory does not require if the editor value to come from an HasTraits
    object. The flip side of that lack of information is that if the value
    refers to a trait, the TraitType information is not available and some
    TraitsUI editors use the trait type to deduce the default editor.
    That might be an acceptable limitation if it can always be easily overcome.

    For example, when editing a list using ListEditor, one needs to
    define the ListEditor like this:

        ListEditor(trait_handler=List(Str()))

    """

    # Editor factory for creating TraitsUI editor.
    editor_factory = Instance("traitsui.editor_factory.EditorFactory")

    # The style used on the factory. (sigh)
    style = Str("simple")

    # Callable to obtain the context for the TraitsUI editor.
    # e.g. populating this dictionary with a key 'key_name' pointing to
    # a HasTraits object allows 'key_name' to be used in the extended names.
    # e.g. ModelView adds 'model' to the context.
    # Callable(ItemHandle) -> dict
    context_getter = Callable(default_value=None, allow_none=None)

    # Whether to make the editor a child of the parent widget
    # and hence making the UI an embedded UI.
    embedded = Bool(True)

    def create(self, parent, item_handle):
        """ Reimplemented BaseItemEditorFactory.create to return a widget
        using TraitsUI editor.
        """
        from traitsui.api import UI, Handler

        # Hold the value in a separate object to defer committing changes.
        holder_object = TraitsUIItemObject(
            value=item_handle.model.get_value(
                item_handle.row, item_handle.column
            ),
        )

        if self.context_getter is not None:
            context = self.context_getter(item_handle)
        else:
            context = {}

        ui = UI(handler=Handler(), context=context)

        factory = getattr(self.editor_factory, self.style + "_editor")
        editor = factory(ui, holder_object, "value", "", parent)
        editor.prepare(parent)
        if self.embedded:
            editor.control.setParent(parent)

        # TraitsUI adds a cycle reference back to 'editor' in the control's
        # '_editor' attribute. This allows cleanup prior to object destruction
        # where the control object that gets passed back to destroy.
        return editor.control

    def commit(self, control, item_handle):
        """ Commit data at the end of an edit.

        Parameters
        ----------
        control : any
            Widget returned by create.
        item_handle : ItemHandle
            The commit action is achieved by assigning value to
            ItemHandle.set_value.
        """
        item_handle.set_value(control._editor.object.value)

    def destroy(self, control):
        """ Implement how to dispose the control created.

        If NotImplementedError is raised, the default behaviour is to
        destroy the control. Override this method to avoid the control
        being destroyed, or to do additional clean up before the control is
        destroyed.
        """
        from traitsui.toolkit import toolkit
        control._editor.dispose()
        toolkit().destroy_control(control)
