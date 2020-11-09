"""

This example shows Kit's interpretation of Corran's design, and is
intended to be constrasted with example_with_modified_lib.py

This example tries to reproduce the functionality in
example_with_modified_lib.py as much as possible.

The only difference here is that the foreground color cannot be set.
Because of that the behaviour related to the foreground color is
different compared to example_with_modified_lib.py

"""

import itertools

from traits.api import (
    Any, Bool, Event, List, Instance, HasStrictTraits, Dict, Callable, observe,
    Property, Str, Int, Enum, Float
)


from pyface.api import ApplicationWindow, GUI
from pyface.color import Color

from pyface.data_view.data_models.api import (
    AttributeDataAccessor, RowTableDataModel,
)
from pyface.data_view.api import (
    AbstractValueType, DataViewSetError,
)

from pyface.data_view.value_types.api import (
    BoolValue, ColorValue, IntValue, TextValue,
)
from pyface.data_view.poc.original_lib_with_custom_editor import (
    NewDataViewWidget,
)
from pyface.data_view.poc.custom_editor import (
    BaseItemEditorFactory,
    TraitsUIItemEditorFactory,
)


class ProposedItemDelegate(HasStrictTraits):
    """ This is the ItemDelegate Corran proposed.
    It is to be defined on the view, by composition.
    In the other design, the ItemDelegate is defined on the data model,
    by composition as well.
    """

    # Callable to test if this delegate can handle the data for the
    # given model, row, column
    # Callable(model, row, column) -> bool
    is_delegate_for = Callable()

    # Factory for creating custom editor.
    item_editor_factory = Instance(BaseItemEditorFactory, allow_none=True)


class BoolValueWithTextEdit(BoolValue):
    """ This extends the original BoolValue to allow the text
    to be edited.

    This contrasts with simply adding from_text in the ItemDelegate
    in the example_with_modified_lib.py example.
    """

    def has_editor_value(self, model, row, column):
        return True

    def get_editor_value(self, model, row, column):
        return self.get_text(model, row, column)

    def set_editor_value(self, model, row, column, value):
        # This assumes the texts are different.
        value = {
            self.true_text.lower(): True,
            self.false_text.lower(): False
        }[value.lower()]
        model.set_value(row, column, value)


class BoolValueWithDropdown(BoolValue):
    """ This extends the original BoolValue to return the bool as editable
    value. Then Qt will use the default dropdown as the editor.
    """

    def has_editor_value(self, model, row, column):
        return True

    # The get_editor_value uses the default implementation on the
    # AbstractValueType (the grandparent class), which just returns the value
    # from the model. That behaviour is what we needed here, because the value
    # would be of a bool type.


class ListStrValue(AbstractValueType):
    """ Currently none of the concrete AbstractValueType in Pyface supports
    a list of values.
    """

    def get_text(self, model, row, column):
        """ Reimplemented AbstractValueType.get_text to return
        the text representation of the list.
        """
        return ",".join(model.get_value(row, column))

    # Original there was a has_editor_value that return false to counter
    # AbstractDataModel.can_set_value returning true, otherwise the default
    # behaviour would be setting the text as a value, which would fail with
    # TraitError as the trait type is a List(Str).
    # Then the method is removed again when the custom editor is introduced,
    # so the custom editor can be launched.


class CSVListStrValue(AbstractValueType):
    """ Subclass so that we can distinguish bg_color_choices and
    fg_color_choices when we want to apply different custom editor to them.
    """

    def get_text(self, model, row, column):
        """ Reimplemented AbstractValueType.get_text to return
        the text representation of the list.
        """
        return ",".join(model.get_value(row, column))


class BgColorValue(AbstractValueType):
    """ This is the value type for the favorite bg color column.

    The ColorValue provided by pyface.data_view.value_types.api assumes
    the underlying value is already an instance of color. Here we want
    to keep the model value as text (color name)
    """

    def has_color(self, model, row, column):
        """ Return true so that get_color is used.

        Note: Initially I forget to add this method - I just added get_color
        and then manually tested the GUI to realize it did nothing.
        """
        return True

    def get_color(self, model, row, column):
        """ Reimplemented to convert the underlying value to an instance of
        Color.

        The view then uses this value to set the background color.
        The foreground color is either white or black depending on how dark
        the background color is.
        """
        return Color.from_str(model.get_value(row, column))


class TextWithBgColorValue(TextValue):
    """ Overridden so that the column for editing greeting can have its
    background color set.
    """

    def has_color(self, model, row, column):
        """ Reimplemented so that it returns true and get_color is used.
        """
        # Note: I forgot to implement this again, even though this
        # is the second time I forgot this (see similar note in
        # BgColorValue.has_color)
        return True

    def get_color(self, model, row, column):
        """ Reimplemented to return an instance of Color so that it gets
        used as background color.
        """
        obj = model.data[row[0]]
        return Color.from_str(obj.favorite_bg_color)


class NewRowTableDataModel(RowTableDataModel):
    """ Override RowTableDataModel so that can_set_value is overridden
    to allow BoolValueWithTextEdit to have editable value.
    """

    def can_set_value(self, row, column):
        """ Overridden RowTableDataModel so that we can selectively disable
        editing of the married flag using the checkbox if the Person age is
        less than 18.
        """
        if len(row) > 0 and len(column) > 0:
            # In order to keep the checkbox visible but to disable it,
            # this logic has to be implemented in can_set_value. This
            # is different from disabling editing the value not via the
            # checkbox.
            column_data = self.column_data[column[0]]
            person = self.data[row[0]]
            # How else can I synchronize without hard-coding and repeating the
            # attribute name? This means this data model is now specific
            # to the Person object specification.
            if column_data.attr == "married":
                return person.age >= 18

            if column_data.attr == "age":
                # For editing age, since we don't have a checkbox, there are
                # actually two other ways to dynamically switch off editing:
                # One can define a new subclass of AbstractValueType and
                # overriden the has_editor_value.
                # Second way is to override get_value_type to return a
                # IntValue with is_editable set to false or true
                return person.is_age_editable

        # For all the other items... each item may still optionally switch
        # them off by defining has_editor_value to return false
        return True


class PersonValue(AbstractValueType):
    """ Subclass for the column that edit an instance of Person.
    """

    def get_text(self, model, row, column):
        """ Reimplemented AbstractValueType.get_text to return
        the text representation of the person.
        """
        return model.get_value(row, column).name


class Person(HasStrictTraits):

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

    married = Bool()

    balance = Float()

    # Instance of Person as well.
    child = Any()


def create_model():
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
    # This tests updating other cell values when a cell is changed.
    # This reveals a bug in RowTableDataModel.set_value.
    def change_greeting(event):
        if not event.new:
            text = "Hello"
        else:
            text = "Congrats"
        for person in objects:
            person.greeting = text

    for person in objects:
        person.observe(change_greeting, "married")

    model = NewRowTableDataModel(
        data=objects,
        row_header_data=AttributeDataAccessor(
            title='multi-line text',
            attr='greeting',
            value_type=TextWithBgColorValue(),
        ),
        column_data = [
            AttributeDataAccessor(
                attr="balance",
                title="float",
                # The implementation text value does what we need:
                # we get the float being represented as text.
                # and the value is edited by the spin box because that
                # is the Qt default when it detects the value is a float
                value_type=TextValue(is_editable=True),
            ),
            AttributeDataAccessor(
                attr="age",
                title="age as range",
                value_type=IntValue(is_editable=True),
            ),
            AttributeDataAccessor(
                attr="age",
                title="age as spinbox",
                value_type=IntValue(is_editable=True),
            ),
            AttributeDataAccessor(
                attr="age",
                title="read only",
                value_type=IntValue(is_editable=False),
            ),
            AttributeDataAccessor(
                attr="is_age_editable",
                title="can edit age?",
                value_type=BoolValueWithTextEdit(
                    true_text="True", false_text="False",
                ),
            ),
            AttributeDataAccessor(
                attr="is_age_editable",
                title="can edit age? (dropdown)",
                value_type=BoolValueWithDropdown(
                    true_text="True", false_text="False",
                ),
            ),
            AttributeDataAccessor(
                attr="married",
                title="married",
                # The checkbox is disabled (but not hidden) if age is less
                # than 18, but that logic does not live in this value_type.
                # That logic lives in the model 'can_set_value' method.
                value_type=BoolValue(true_text="Yes", false_text="No"),
            ),

            AttributeDataAccessor(
                attr="favorite_bg_color",
                title="bg color",
                value_type=BgColorValue(),
            ),

            AttributeDataAccessor(
                attr="bg_color_choices",
                title="bg color choices",
                value_type=ListStrValue(),
            ),

            AttributeDataAccessor(
                attr="favorite_fg_color",
                title="fg color",
                # No idea how foreground color is supposed to be supported.
                value_type=TextValue(is_editable=False),
            ),

            AttributeDataAccessor(
                attr="fg_color_choices",
                title="fg color choices",
                value_type=CSVListStrValue(),
            ),

            AttributeDataAccessor(
                attr="child",
                title="child",
                value_type=PersonValue(),
            ),
        ],
    )
    return model



class MainWindow(ApplicationWindow):

    def _create_contents(self, parent):

        # Use traitsui editor for proof-of-concept.
        from traitsui.api import (
            RangeEditor, ListEditor, CSVListEditor, InstanceEditor,
            TextEditor,
        )

        data_model = create_model()
        widget = NewDataViewWidget(
            parent=parent,
            data_model=data_model,
            selection_mode="none",
            item_delegates=[
                # Use custom TextEditor for the row header
                # Previously this uses column index in is_delegate_for as
                # there are many TextValue here and isinstance check would not
                # be enough. But then the text needs to have a background
                # color, so a new subclass is created for the column, and
                # we can use isinstance check again. Still a smell, though.
                ProposedItemDelegate(
                    is_delegate_for=lambda model, row, column: (
                        isinstance(
                            model.get_value_type(row, column),
                            TextWithBgColorValue,
                        )
                    ),
                    item_editor_factory=TraitsUIItemEditorFactory(
                        style="custom",
                        editor_factory=TextEditor(),
                    )
                ),
                # Use RangeEditor for one of the columns
                # editing an integer. Can't use isinstance because there
                # is another IntValue we don't want to use RangeEditor.
                # Alternatively is to create another subclass of value type
                # just so that the isinstance change can be more specific.
                ProposedItemDelegate(
                    is_delegate_for=lambda model, row, column: (
                        column == (1, )
                    ),
                    item_editor_factory=TraitsUIItemEditorFactory(
                        editor_factory=RangeEditor(low=0, high=100),
                    )
                ),
                # This, I believe, is what Corran thinks is the most common
                # use case: is_delegate_for does isinstance check.
                # But this assumes all ListStrValue uses the same custom
                # editor.
                # After I added this, the item editor could not be used,
                # because I forgot to remove the overridden
                # ListStrValue.has_editor_value so that it falls back
                # to returning the value from AbstractDataValue.can_set_value.
                ProposedItemDelegate(
                    is_delegate_for=lambda model, row, column: (
                        isinstance(
                            model.get_value_type(row, column),
                            ListStrValue,
                        )
                    ),
                    item_editor_factory=TraitsUIItemEditorFactory(
                        editor_factory=ListEditor(
                            trait_handler=List(Str()),
                        ),
                    )
                ),
                ProposedItemDelegate(
                    is_delegate_for=lambda model, row, column: (
                        isinstance(
                            model.get_value_type(row, column),
                            CSVListStrValue,
                        )
                    ),
                    item_editor_factory=TraitsUIItemEditorFactory(
                        editor_factory=CSVListEditor(),
                    )
                ),
                ProposedItemDelegate(
                    is_delegate_for=lambda model, row, column: (
                        isinstance(
                            model.get_value_type(row, column),
                            PersonValue,
                        )
                    ),
                    item_editor_factory=TraitsUIItemEditorFactory(
                        style="custom",
                        embedded=False,   # so it pops up
                        editor_factory=InstanceEditor(),
                    )
                ),
            ]
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
