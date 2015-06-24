# Standard library imports.
import unittest

# Enthought library imports.
from traits.etsconfig.api import ETSConfig
from pyface.tasks.api import Editor, EditorAreaPane

USING_WX = ETSConfig.toolkit not in ['', 'qt4']


class EditorAreaPaneTestCase(unittest.TestCase):

    @unittest.skipIf(USING_WX, "EditorAreaPane is not implemented in WX")
    def test_create_editor(self):
        """ Does creating an editor work?
        """
        area = EditorAreaPane()
        area.register_factory(Editor, lambda obj: isinstance(obj, int))
        self.assert_(isinstance(area.create_editor(0), Editor))

    @unittest.skipIf(USING_WX, "EditorAreaPane is not implemented in WX")
    def test_factories(self):
        """ Does registering and unregistering factories work?
        """
        area = EditorAreaPane()
        area.register_factory(Editor, lambda obj: isinstance(obj, int))
        self.assertEqual(area.get_factory(0), Editor)
        self.assertEqual(area.get_factory('foo'), None)

        area.unregister_factory(Editor)
        self.assertEqual(area.get_factory(0), None)


if __name__ == '__main__':
    unittest.main()
