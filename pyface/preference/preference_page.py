# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for all preference pages. """


from traits.api import HasTraits


# fixme: in JFace this extends from 'DialogPage' which we don't have yet!
class PreferencePage(HasTraits):
    """ Abstract base class for all preference pages. """

    # ------------------------------------------------------------------------
    # 'PreferencePage' interface.
    # ------------------------------------------------------------------------

    def create_control(self, parent):
        """ Creates the toolkit-specific control for the page. """

        raise NotImplementedError()

    def restore_defaults(self):
        """ Restore the default preferences. """

        pass

    def show_help_topic(self):
        """ Show the help topic for this preference page."""

        pass
