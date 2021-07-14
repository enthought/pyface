# (C) Copyright 2005-2021 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Wizard example. """


import os
import sys

# Put the Enthought library on the Python path.
sys.path.append(os.path.abspath(r"..\..\.."))


from pyface.api import GUI, OK
from pyface.wizard.api import SimpleWizard, WizardPage
from traits.api import Color, HasTraits, Int, Str


class Details(HasTraits):
    """ Some test data. """

    name = Str()
    color = Color


class SimpleWizardPage(WizardPage):
    """ A simple wizard page. """

    # 'SimpleWizardPage' interface -----------------------------------------

    # The page color.
    color = Color

    # ------------------------------------------------------------------------
    # 'IWizardPage' interface.
    # ------------------------------------------------------------------------

    def _create_page_content(self, parent):
        """ Create the wizard page. """

        details = Details(color=self.color)
        details.observe(self._on_name_changed, "name")

        return details.edit_traits(parent=parent, kind="subpanel").control

    # ------------------------------------------------------------------------
    # Private interface.
    # ------------------------------------------------------------------------

    # Trait event handlers -------------------------------------------------

    def _on_name_changed(self, event):
        """ Called when the name has been changed. """

        self.complete = len(event.new.strip()) > 0

        return


# Application entry point.
if __name__ == "__main__":
    # Create the GUI (this does NOT start the GUI event loop).
    gui = GUI()

    wizard = SimpleWizard(
        parent=None,
        title="Create something magical",
        pages=[
            SimpleWizardPage(
                id="foo",
                color="red",
                heading="The Red Page",
                subheading="The default color on this page is red.",
            ),
            SimpleWizardPage(
                id="bar",
                color="yellow",
                heading="The Yellow Page",
                subheading="The default color on this page is yellow.",
            ),
            SimpleWizardPage(
                id="baz",
                color="green",
                heading="The Green Page",
                subheading="The default color on this page is green.",
            ),
        ],
    )

    # Create and open the wizard.
    if wizard.open() == OK:
        print("Wizard completed successfully")
    else:
        print("Wizard cancelled")
