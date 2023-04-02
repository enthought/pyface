# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from pyface.tasks.editor import Editor
from pyface.tasks.enaml_pane import EnamlPane


class EnamlEditor(EnamlPane, Editor):
    """ Create an Editor for Enaml Components. """
