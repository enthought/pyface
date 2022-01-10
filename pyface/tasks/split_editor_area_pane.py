# (C) Copyright 2005-2022 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""
- :attr:`~.SplitEditorAreaPane`
- :attr:`~.EditorAreaWidget`
"""

from pyface.toolkit import toolkit_object

SplitEditorAreaPane = toolkit_object(
    "tasks.split_editor_area_pane:" "SplitEditorAreaPane"
)

EditorAreaWidget = toolkit_object(
    "tasks.split_editor_area_pane:" "EditorAreaWidget"
)
