#-----------------------------------------------------------------------------
#
#  Copyright (c) 2005-2006 by Enthought, Inc.
#  All rights reserved.
#
#  Author: David C. Morrill <dmorrill@enthought.com>
#
#-----------------------------------------------------------------------------
""" Object with views for naming or renaming a user perspective. """


# Enthought library imports.
from traits.api import Bool, HasTraits, Trait, TraitError, Constant
from traitsui.api import View, Item, VGroup
import six


#### Trait definitions ########################################################

def not_empty_string(object, name, value):
    """a not-empty string"""

    if isinstance(value, six.string_types) and (value.strip() != ''):
        return value

    raise TraitError

# Define a trait which can not be the empty string:
NotEmptyString = Trait('', not_empty_string)


class UserPerspectiveName(HasTraits):
    """ Object with views for naming or renaming a user perspective. """

    ###########################################################################
    # 'UserPerspectiveName' interface.
    ###########################################################################

    # The name of the new user perspective.
    name = NotEmptyString

    # Should the editor area be shown in this perpsective?
    show_editor_area = Bool(True)

    # Help notes when creating a new view.
    new_help = Constant("""Note:
 - The new perspective will initially be empty.
 - Add new views to the perspective by selecting
   them from the 'View' menu.
 - Drag the notebook tabs and splitter bars to
   arrange the views within the perspective.""")

    #### Traits views #########################################################

    new_view = View(
        VGroup(
            VGroup( 'name', 'show_editor_area' ),
            VGroup( '_',
                Item( 'new_help',
                      style = 'readonly' ),
                show_labels = False
            )
        ),
        title   = 'New User Perspective',
        id      = 'envisage.workbench.action.'
                  'new_user_perspective_action.UserPerspectiveName',
        buttons = [ 'OK', 'Cancel' ],
        kind    = 'livemodal',
        width   = 300
    )

    save_as_view = View( 'name',
        title   = 'Save User Perspective As',
        id      = 'envisage.workbench.action.'
                  'save_as_user_perspective_action.UserPerspectiveName',
        buttons = [ 'OK', 'Cancel' ],
        kind    = 'livemodal',
        width   = 300
    )

    rename_view = View( 'name',
        title   = 'Rename User Perspective',
        id      = 'envisage.workbench.action.'
                  'rename_user_perspective_action.UserPerspectiveName',
        buttons = [ 'OK', 'Cancel' ],
        kind    = 'livemodal',
        width   = 300
    )

#### EOF #####################################################################

