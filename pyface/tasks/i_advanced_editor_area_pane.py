# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.tasks.i_editor_area_pane import IEditorAreaPane


class IAdvancedEditorAreaPane(IEditorAreaPane):
    """ A splitable central pane that contains tabbed editors.
    """

    # ------------------------------------------------------------------------
    # 'IAdvancedEditorAreaPane' interface.
    # ------------------------------------------------------------------------

    def get_layout(self):
        """ Returns a LayoutItem that reflects the current state of the editors.

        Because editors do not have IDs, they are identified by their index in
        the list of editors. For example, PaneItem(0) refers to the first
        editor.

        If there are no open editors, returns None.
        """

    def set_layout(self, layout):
        """ Applies a LayoutItem to the editors in the pane.

        The layout should have panes with IDs as described in ``get_layout()``.
        For example, if one wanted to open two editors side by side, with the
        first to the left of the right, something like this would appropriate::

            editor_area.edit(File('foo.py'))
            editor_area.edit(File('bar.py'))
            editor_area.set_layout(VSplitter(PaneItem(0),
                                             PaneItem(1)))

        Editors that are not included in the layout will be tabbified with other
        editors in an undefined manner.

        If the layout is None, this method is a no-op. Hence it is always safe
        to call this method with the results of ``get_layout()``.
        """
