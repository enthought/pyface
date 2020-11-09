""" This file shows building a table example using the modified core code.

The example demonstrates various ways to customize how a cell is displayed
and edited.
"""
import enum
from functools import partial
import itertools

from traits.api import (
    Any, Bool, Event, List, Instance, HasStrictTraits, Dict, Callable, observe,
    Property, Str, Int, Enum, Float
)


from pyface.api import ApplicationWindow, GUI


from pyface.data_view.abstract_value_type import CheckState

from pyface.color import Color


from pyface.data_view.api import DataViewSetError, DataViewGetError


from pyface.data_view.poc.modified_lib import (
    NewAttributeDataAccessor,
    NewRowTableDataModel,
    NewDataViewWidget,
    ItemDelegate,
)

from pyface.data_view.poc.custom_editor import (
    TraitsUIItemEditorFactory,
)


def bool_to_check_state(item_handle, value):
    """ Basic mapping from value to CheckState."""
    if bool(value):
        return CheckState.CHECKED
    return CheckState.UNCHECKED


def check_state_to_bool(item_handle, value):
    """ Basic mapping from CheckState back to bool."""
    return value == CheckState.CHECKED


def validate_fg_color(item_handle, text):
    """ validator for editing the foreground color as text.
    """
    try:
        Color.from_str(text)
    except Exception:
        return False
    else:
        person = item_handle.model.data[item_handle.row[0]]
        return text in person.fg_color_choices


class Person(HasStrictTraits):
    """ This object represents the business/domain specific data model.
    """

    name = Str()

    age = Int()

    # This demonstrates overriding editable state.
    # If false, the range editor for editing age cannot be open.
    is_age_editable = Bool(True)

    favorite_bg_color = Enum(values="bg_color_choices")

    bg_color_choices = List(Str(), ["red", "blue", "black"])

    favorite_fg_color = Enum(values="fg_color_choices")

    fg_color_choices = List(Str(), ["yellow", "grey", "white"])

    greeting = Str("Hello")

    balance = Float()

    married = Bool()

    # Instance of Person as well.
    child = Any()


def create_model():
    """ Return the object to be used with the DataViewWidget.

    This object is close to the Presentation Model described by Martin Fowler.
    This makes the GUI toolkit specific view really dumb.

    Returns
    -------
    model : AbstractDataModel
    """

    # demonstrate using TraitsUI editor in ItemDelegate
    from traitsui.api import (
        EnumEditor, TextEditor, RangeEditor, InstanceEditor, ListEditor,
        CSVListEditor,
    )

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
        NewAttributeDataAccessor(
            # This edits the Person instance with the InstanceEditor.
            attr="balance",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "float",
            ),
            value_item_delegate=ItemDelegate(
                # We use the default spinbox editor from Qt.
                to_editable_value=lambda _, value: value,
                from_editable_value=lambda _, value: value,
            ),
        ),
        NewAttributeDataAccessor(
            attr="age",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "age as range",
            ),
            # This shows using the RangeEditor as custom editor.
            value_item_delegate=ItemDelegate(
                validator=lambda _, value: value <= 100,
                is_editable=lambda handle: (
                    handle.model.data[handle.row[0]].is_age_editable
                ),
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=RangeEditor(low=0, high=100),
                )
            ),
        ),
        NewAttributeDataAccessor(
            attr="age",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "age in spinbox",
            ),
            value_item_delegate=ItemDelegate(
                is_editable=lambda handle: (
                    handle.model.data[handle.row[0]].is_age_editable
                ),
                # This returns a int, and will use the default Qt spinbox
                # widget for editing.
                to_editable_value=lambda _, value: value,
                from_editable_value=lambda _, value: value,
            ),
        ),
        NewAttributeDataAccessor(
            attr="age",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "read only",
            ),
            # default value_item_delegate is a non-editable text.
        ),
        NewAttributeDataAccessor(
            attr="is_age_editable",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "can edit age?",
            ),
            value_item_delegate=ItemDelegate(
                to_editable_value=lambda _, value: str(value),
                from_editable_value=lambda _, value: (
                    {"true": True, "false": False}[value.lower()]
                ),
                to_check_state=bool_to_check_state,
                from_check_state=check_state_to_bool,
            ),
        ),
        NewAttributeDataAccessor(
            attr="is_age_editable",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "can edit age? (dropdown)",
            ),
            value_item_delegate=ItemDelegate(
                # This returns a bool type value, and Qt will use a dropdown
                to_editable_value=lambda _, value: value,
                from_editable_value=lambda _, value: value,
                to_check_state=bool_to_check_state,
                from_check_state=check_state_to_bool,
            ),
        ),
        NewAttributeDataAccessor(
            attr="married",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "married",
            ),
            # This shows the checkbox along with editing text to be converted to
            # bool.
            value_item_delegate=ItemDelegate(
                is_editable=lambda handle: (
                    # only editable if the person has come of age.
                    handle.model.data[handle.row[0]].age >= 18
                ),
                to_display_text=lambda _, value: {True: "Yes", False: "No"}[value],
                to_check_state=bool_to_check_state,
                from_check_state=check_state_to_bool,
            ),
        ),
        NewAttributeDataAccessor(
            attr="favorite_bg_color",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "bg color",
            ),
            # This shows using EnumEditor and having the options dynamically
            # updated.
            value_item_delegate=ItemDelegate(
                to_bg_color=lambda _, value: Color.from_str(value),
                item_editor_factory=TraitsUIItemEditorFactory(
                    style="custom",
                    editor_factory=EnumEditor(
                        mode="radio",
                        name="person.bg_color_choices",
                    ),
                    context_getter=lambda handle: (
                        {"person": handle.model.data[handle.row[0]]}
                    ),
                )
            ),
        ),
        NewAttributeDataAccessor(
            attr="bg_color_choices",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "bg color choices",
            ),
            value_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: ",".join(value),
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=ListEditor(
                        # Otherwise the editor does not know what
                        # item editor to use.
                        trait_handler=List(Str()),
                    ),
                ),
            ),
        ),
        NewAttributeDataAccessor(
            attr="favorite_fg_color",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "fg color",
            ),
            # Edit fg color with text.
            value_item_delegate=ItemDelegate(
                to_bg_color=lambda _, value: (
                    Color.from_str("white") if Color.from_str(value).is_dark
                    else Color.from_str("black")
                ),
                to_fg_color=lambda _, value: Color.from_str(value),
                validator=validate_fg_color,
                from_editable_value=lambda _, value: value,
            ),
        ),
        NewAttributeDataAccessor(
            attr="fg_color_choices",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "fg color choices",
            ),
            value_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: ",".join(value),
                to_editable_value=lambda _, value: ",".join(value),
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=CSVListEditor(),
                ),
            ),
        ),
        NewAttributeDataAccessor(
            # This edits the Person instance with the InstanceEditor.
            attr="child",
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "child",
            ),
            value_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: value.name,
                item_editor_factory=TraitsUIItemEditorFactory(
                    style="custom",
                    embedded=False,   # so it pops up
                    editor_factory=InstanceEditor(),
                ),
            ),
        ),
    ]

    model = NewRowTableDataModel(
        data=objects,
        row_header_data=NewAttributeDataAccessor(
            attr='greeting',
            title="this 'title' trait is redundant",
            title_item_delegate=ItemDelegate(
                to_display_text=lambda _, value: "multi-line text",
            ),
            # This shows using the custom multi-line text editor.
            value_item_delegate=ItemDelegate(
                validator=lambda _, value: len(value) > 0,
                to_bg_color=lambda item_handle, _: (
                    Color.from_str(item_handle.model.data[item_handle.row[0]].favorite_bg_color)
                ),
                to_fg_color=lambda item_handle, _: (
                    Color.from_str(item_handle.model.data[item_handle.row[0]].favorite_fg_color)
                ),
                to_editable_value=lambda _, value: value,
                item_editor_factory=TraitsUIItemEditorFactory(
                    editor_factory=TextEditor(),
                    style="custom",
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
