import enum
from functools import partial
import itertools

from traits.api import (
    Any, Bool, Event, List, Instance, HasStrictTraits, Dict, Callable, observe,
    Property, Str, Int, Enum, Float, Range, File, Tuple, Date, Datetime,
    Time,
)
from traits.observation.api import trait
from traitsui.api import Font

from pyface.api import ApplicationWindow, GUI
from pyface.color import Color
from pyface.data_view.abstract_value_type import CheckState
from pyface.data_view.data_models.api import RowTableDataModel
from pyface.data_view.data_models.data_accessors import AttributeDataAccessor
from pyface.data_view.api import DataViewSetError, DataViewGetError

from pyface.data_view.poc.modified_lib import (
    NewDataViewWidget,
    ItemDelegate,
)

from pyface.data_view.poc.custom_editor import (
    TraitsUIItemEditorFactory,
    FileDialogItemEditorFactory,
)


def _xget_context(obj, extended_name):
    """ Parse the extended name to return object and the simple trait name
    (which is the last segment).

    e.g. "a.b.c" will return the object referred to by "a.b", along with the
    trait name "c"

    Parameters
    ----------
    obj : obj
        The object on which the extended name is defined one.
    extended_name : str
        Dot separated name, e.g. 'a.b.c'.

    Returns
    -------
    context_obj : object
        The object on which the last segment applies for obtaining attribute
        value.
    name : str
        The required attribute name on context_obj.
    """
    context_obj = obj
    parts = extended_name.split(".")

    for part in parts[:-1]:
        context_obj = getattr(context_obj, part)

    name = parts[-1]
    return context_obj, name


def default_item_delegate_setting(object, trait):
    """ Return default settings of an ItemDelegate for a given CTrait
    instance and the object it is associated with.

    Parameters
    ----------
    object : HasTraits
        Object on which the trait is defined one.
    trait : CTrait
        The trait for which the ItemDelegate is created.

    Returns
    -------
    settings : dict
        Keyword arguments for instantiating a default ItemDelegate for the
        given trait.
    """
    from traitsui.api import InstanceEditor, FileEditor
    _trait_type_to_delegate_spec = {
        # Just show a checkbox for boolean value.
        Bool: dict(
            to_display_text=lambda _, value: "",
            to_check_state=lambda _, value: {
                True: CheckState.CHECKED, False: CheckState.UNCHECKED
            }[value],
            from_check_state=lambda _, value: value == CheckState.CHECKED,
            item_editor_factory=None,
        ),
        # The simple instance editor requires another button click.
        # Use the custom one instead, and don't embed it because it is
        # often too big to fit.
        Instance: dict(
            item_editor_factory=TraitsUIItemEditorFactory(
                embedded=False,
                style="custom",
                editor_factory=InstanceEditor(),
            ),
        ),
        # Cannot use the simple FileEditor. Simple FileEditor is a widget
        # containing another textbox and a button for launching a file dialog.
        # As soon as a file dialog is opened, the focus is lost and the editor
        # is closed. Instead, the editor has to be the modal dialog itself.
        File: dict(
            item_editor_factory=FileDialogItemEditorFactory(
                mode=(
                    "open" if getattr(trait.trait_type, "exists", False)
                    else "save"
                ),
            ),
        ),
        # For List trait, the editor widget is given the size that fits the
        # current content, which could be too small in some cases. Not sure if
        # it is possible to make the editor widget resize as its content
        # changes.
    }
    result = dict(
        to_editable_value=lambda _, value: value,
        item_editor_factory=TraitsUIItemEditorFactory(
            editor_factory=trait.get_editor(),
            context_getter=lambda handle: {"object": object}
        )
    )
    result.update(_trait_type_to_delegate_spec.get(
        trait.trait_type.__class__, {})
    )
    return result


class TraitedAttributeDataAccessor(AttributeDataAccessor):
    """ Overridden AttributeDataAccessor to demonstrate the following
    features:

    - Add/Remove observers for updating the view when a trait is changed
      externally.
    - Provide a good default ItemDelegate with the given trait definition.
    - Allow overriding ItemDelegate setting easily.
    """

    # Keyword arguments for overriding various attributes on the ItemDelegate.
    extra_delegate_settings = Dict()

    def get_value_item_delegate(self, object):
        """ Return an instance of ItemDelegate for displaying and editing
        the attribute (defined on this accessor) for the given object.

        Returns
        -------
        value_item_delegate : ItemDelegate
        """
        context_object, name = _xget_context(object, self.attr)
        trait = context_object.trait(name=name)
        delegate_settings = (
            default_item_delegate_setting(context_object, trait)
        )
        delegate_settings.update(self.extra_delegate_settings)
        return ItemDelegate(**delegate_settings)

    def _fire_value_change(self, _):
        self.updated = (self, "value")

    def _add_observer(self, object):
        object.observe(self._fire_value_change, self.attr)

    def _remove_observer(self, object):
        object.observe(self._fire_value_change, self.attr, remove=True)


class TraitedRowTableDataModel(RowTableDataModel):
    """ Extend RowTableDataModel to support:

    - Hooking up observers so that view can update when a trait is changed
      externally.
    """

    def traits_init(self):
        """ Set up observers after the model is initialized.
        """
        self._add_observer(self.data)

    def _get_all_accessors(self):
        """ Return all the accessors (i.e. row header + columns)
        """
        if self.row_header_data is not None:
            accessors = [self.row_header_data]
        else:
            accessors = []
        return accessors + self.column_data

    def _add_observer(self, objects):
        """ Add observers for the given list of objects."""
        for item in objects:
            for accessor in self._get_all_accessors():
                accessor._add_observer(item)

    def _remove_observer(self, objects):
        """ Remove observers for the given list of objects."""
        for item in objects:
            for accessor in self._get_all_accessors():
                accessor._remove_observer(item)

    @observe(trait("data", notify=False).list_items(optional=True))
    def _update_item_observer(self, event):
        """ When the list of objects is mutated, remove observers for the
        removed items, add observers for the added items.
        """
        self._remove_observer(event.removed)
        self._add_observer(event.added)

    @observe("data", post_init=True)
    def _update_data_observer(self, event):
        """ When the entire data is changed, remove observers for all the
        old values, add observers for all the new values.
        """
        self._remove_observer(event.old)
        self._add_observer(event.new)

    @observe("column_data:items")
    def _handle_column_data_items_change(self, event):
        """ When the columns are mutated, remove observers for the removed
        column(s), add observers for the added column(s).
        """
        for accessor in event.removed:
            accessor._remove_observer(self.data)
        for accessor in event.added:
            accessor._add_observe(self.data)

    # This observer assumes all accessors are AttributeDataAccessor.
    # But how else are we going to remove observers when 'attr' is mutated?
    # Does 'attr' really have to be mutable, though?
    @observe("column_data:items:attr")
    @observe("row_header_data:attr")
    def _handle_observer_when_attr_change(self, event):
        """ Assuming all accessors are AttributeDataAccessor here...
        If the 'attr' is mutated, synchronize the observers too.
        """
        accessor = event.object
        for obj in self.data:
            obj.observe(accessor._fire_value_change, event.old, remove=True)
        for obj in self.data:
            obj.observe(accessor._fire_value_change, event.new)

    def get_value_type(self, row, column):
        raise RuntimeError("Remove value type from model.")

    def get_item_delegate(self, row, column):
        """ Return the ItemDelegate that holds the information about how
        an item is displayed and edited.
        """
        if len(column) == 0:
            column_data = self.row_header_data
        else:
            column_data = self.column_data[column[0]]

        if len(row) == 0:
            return ItemDelegate(to_display_text=lambda _, v: column_data.title)

        # NOTE: Instead of having `value_item_delegate` being just a value,
        # we need it to be a method so that it can be dynamically computed
        # based on the object.
        return column_data.get_value_item_delegate(self.data[row[0]])

    def can_set_value(self, row, column):
        raise RuntimeError("I am not needed any more")


class Person(HasStrictTraits):
    """ This object represents the business/domain specific data model.
    """

    name = Str()

    age = Range(low=0, high=100)

    dead = Bool()

    favorite_bg_color = Enum(values="bg_color_choices")

    bg_color_choices = List(Str(), ["red", "blue", "black"])

    favorite_fg_color = Enum(values="fg_color_choices")

    fg_color_choices = List(Str(), ["yellow", "grey", "white"])

    greeting = Str("Hello")

    balance = Float(100.0)

    married = Bool()

    config_file = File(exists=True)

    post_code = Tuple(Str("M3"), Str("9AR"))

    birthday = Date()

    birth_time = Time()

    appointment_time = Datetime()

    is_broke = Property(Bool())

    def _get_is_broke(self):
        return self.balance < 10.0


Person.add_class_trait("child", Instance(Person))


def create_model():
    """ Return the object to be used with the DataViewWidget.

    This object is close to the Presentation Model described by Martin Fowler.
    This makes the GUI toolkit specific view really dumb.

    Returns
    -------
    model : AbstractDataModel
    """

    names = itertools.cycle(["John", "Mary", "Peter"])
    child_names = itertools.cycle(["Paul", "Joey", "Alex"])
    bg_colors = itertools.cycle(["red", "blue", "black"])
    fg_colors = itertools.cycle(["yellow", "grey", "white"])
    objects = [
        Person(
            name=next(names),
            favorite_bg_color=next(bg_colors),
            favorite_fg_color=next(fg_colors),
            child=Person(name=next(child_names)),
        )
        for _ in range(1000)
    ]

    # If any person is married, change the greeting
    def change_greeting(event):
        if not event.new:
            text = "Hello"
        else:
            text = "Congrats"
        for person in objects:
            person.greeting = text

    for person in objects:
        person.observe(change_greeting, "married")

    column_data = [
        TraitedAttributeDataAccessor(
            attr="balance",
            title="Acc. balance",
        ),
        TraitedAttributeDataAccessor(
            attr="is_broke",
            extra_delegate_settings=dict(
                # Hitting the limit of introspection here.
                # The property is a transient trait but there is no public way
                # to tell if the trait is settable... unless we want to detect
                # for magically named method on the object.
                is_editable=lambda _: False,
            ),
        ),
        TraitedAttributeDataAccessor(
            attr="age",
            extra_delegate_settings=dict(
                is_editable=lambda handle: (
                    not handle.model.data[handle.row[0]].dead
                ),
            ),
        ),
        TraitedAttributeDataAccessor(
            attr="married",
            extra_delegate_settings=dict(
                is_editable=lambda handle: (
                    not handle.model.data[handle.row[0]].dead
                    and handle.model.data[handle.row[0]].age >= 18
                ),
            ),
        ),
        TraitedAttributeDataAccessor(
            attr="dead",
        ),
        TraitedAttributeDataAccessor(
            attr="favorite_bg_color",
        ),
        TraitedAttributeDataAccessor(
            attr="bg_color_choices",
            extra_delegate_settings=dict(
                to_display_text=lambda _, value: ", ".join(value),
            ),
        ),
        TraitedAttributeDataAccessor(
            attr="favorite_fg_color",
        ),
        TraitedAttributeDataAccessor(
            attr="fg_color_choices",
            extra_delegate_settings=dict(
                to_display_text=lambda _, value: ",".join(value),
            ),
        ),
        TraitedAttributeDataAccessor(
            attr="config_file",
        ),
        TraitedAttributeDataAccessor(
            attr="post_code",
            extra_delegate_settings=dict(
                validator=lambda _, value: all(part for part in value),
                to_display_text=lambda _, value: " ".join(value),
            ),
        ),
        TraitedAttributeDataAccessor(
            attr="birthday",
        ),
        TraitedAttributeDataAccessor(
            attr="birth_time",
        ),
        TraitedAttributeDataAccessor(
            attr="child",
            extra_delegate_settings=dict(
                to_display_text=lambda _, value: value.name,
            ),
        ),
    ]

    model = TraitedRowTableDataModel(
        data=objects,
        row_header_data=TraitedAttributeDataAccessor(
            attr='greeting',
            extra_delegate_settings=dict(
                to_bg_color=lambda item_handle, _: (
                    Color.from_str(item_handle.model.data[item_handle.row[0]].favorite_bg_color)
                ),
                to_fg_color=lambda item_handle, _: (
                    Color.from_str(item_handle.model.data[item_handle.row[0]].favorite_fg_color)
                ),
            ),
        ),
        column_data=column_data,
    )

    return model


class MainWindow(ApplicationWindow):
    """ This is the very dumb 'View' """

    def _create_contents(self, parent):
        data_model = create_model()
        widget = NewDataViewWidget(
            parent=parent,
            data_model=data_model,
            selection_mode='none',
        )
        widget._create()
        return widget.control


def run():
    window = MainWindow()
    window._create()
    window.show(True)
    window.open()
    GUI().start_event_loop()


if __name__ == "__main__":
    run()
