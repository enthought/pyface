# (C) Copyright 2005-2020 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

import unittest


from traits.etsconfig.api import ETSConfig
from pyface.tasks.api import Editor, EditorAreaPane

USING_WX = ETSConfig.toolkit not in ["", "qt4"]


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
        self.assertEqual(area.get_factory("foo"), None)

        area.unregister_factory(Editor)
        self.assertEqual(area.get_factory(0), None)


if __name__ == "__main__":
    unittest.main()
