#------------------------------------------------------------------------------
# Copyright (c) 2005, Enthought, Inc.
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
# Thanks for using Enthought open source!
#
# Author: Enthought, Inc.
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
from .i_wizard_page import IWizardPage
from .wizard_page import WizardPage

from .i_wizard import IWizard
from .wizard import Wizard

from .i_wizard_controller import IWizardController
from .wizard_controller import WizardController

from .chained_wizard import ChainedWizard
from .chained_wizard_controller import ChainedWizardController

# These are deprecated.  Use Wizard and WizardController instead.
from .simple_wizard import SimpleWizard
from .simple_wizard_controller import SimpleWizardController
