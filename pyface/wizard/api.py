# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

"""

API for the ``pyface.wizard`` subpackage.

- :class:`~.WizardPage`
- :class:`~.Wizard`
- :class:`~.WizardController`
- :class:`~.ChainedWizard`
- :class:`~.ChainedWizardController`

Interfaces
----------

- :class:`~.IWizardPage`
- :class:`~.IWizard`
- :class:`~.IWizardController`

"""

from .chained_wizard_controller import ChainedWizardController
from .i_wizard_page import IWizardPage
from .i_wizard import IWizard
from .i_wizard_controller import IWizardController
from .wizard_controller import WizardController


# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

_toolkit_imports = {
    'Wizard': 'wizard',
    'WizardPage': 'wizard_page',
}

# These are pyface.* imports that have selection as a side-effect
_relative_imports = {
    'ChainedWizard': "chained_wizard",
}


def __getattr__(name):
    """Lazily load attributes with side-effects

    In particular, lazily load toolkit backend names.  For efficiency, lazily
    loaded objects are injected into the module namespace
    """
    # sentinel object for no result
    not_found = object()
    result = not_found

    if name in _relative_imports:
        from importlib import import_module
        source = _relative_imports[name]
        module = import_module(f"pyface.wizard.{source}")
        result = getattr(module, name)

    elif name in _toolkit_imports:
        from pyface.toolkit import toolkit_object
        source = _toolkit_imports[name]
        result = toolkit_object(f"wizard.{source}:{name}")

    if result is not_found:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    globals()[name] = result
    return result


# ----------------------------------------------------------------------------
# Introspection support
# ----------------------------------------------------------------------------

# the list of available names we report for introspection purposes
_extra_names = set(_toolkit_imports) | set(_relative_imports)


def __dir__():
    return sorted(set(globals()) | _extra_names)
