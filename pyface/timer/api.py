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

API for the ``pyface.timer`` subpackage.

- :func:`~.do_later`
- :func:`~.do_after`
- :class:`~.DoLaterTimer`
- :class:`~.CallbackTimer`
- :class:`~.EventTimer`
- :class:`~.Timer`

Interfaces
----------
- :class:`~.ICallbackTimer`
- :class:`~.IEventTimer`
- :class:`~.ITimer`

"""

from .i_timer import ICallbackTimer, IEventTimer, ITimer


# ----------------------------------------------------------------------------
# Deferred imports
# ----------------------------------------------------------------------------

# These imports have the side-effect of performing toolkit selection

# These are pyface.undo.* imports that have selection as a side-effect
# TODO: refactor to delay imports where possible
_relative_imports = {
    'do_later': 'do_later',
    'do_after': 'do_later',
    'DoLaterTimer': 'do_later',
    'CallbackTimer': 'timer',
    'EventTimer': 'timer',
    'Timer': 'timer',
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
        module = import_module(f"pyface.timer.{source}")
        result = getattr(module, name)

    if result is not_found:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    globals()[name] = result
    return result


# ----------------------------------------------------------------------------
# Introspection support
# ----------------------------------------------------------------------------

def __dir__():
    return sorted(set(globals()) | set(_relative_imports))
