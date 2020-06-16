from unittest import TestCase
from unittest.mock import Mock

from ..text_value import TextValue


class TestTextValue(TestCase):

    def setUp(self):
        self.model = Mock()
        self.model.get_value = Mock(return_value="test")
        self.model.can_set_value = Mock(return_value=True)
        self.model.set_value = Mock(return_value=True)

    def test_defaults(self):
        value = TextValue()
        self.assertTrue(value.is_editable)

    def test_is_valid(self):
        value = TextValue()
        self.assertTrue(value.is_valid(None, [0], [0], "test"))

    def test_get_editable(self):
        value = TextValue()
        editable = value.get_editable(self.model, [0], [0])

        self.assertEqual(editable, "test")

    def test_set_editable(self):
        value = TextValue()
        success = value.set_editable(self.model, [0], [0], "test")

        self.assertTrue(success)
        self.model.set_value.assert_called_once_with([0], [0], "test")

    def test_get_text(self):
        value = TextValue()
        editable = value.get_text(self.model, [0], [0])

        self.assertEqual(editable, "test")

    def test_set_text(self):
        value = TextValue()
        success = value.set_text(self.model, [0], [0], "test")

        self.assertTrue(success)
        self.model.set_value.assert_called_once_with([0], [0], "test")

