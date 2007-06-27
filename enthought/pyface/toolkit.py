#------------------------------------------------------------------------------
# Copyright (c) 2007, Riverbank Computing Limited
# All rights reserved.
# 
# This software is provided without warranty under the terms of the BSD
# license included in enthought/LICENSE.txt and may be redistributed only
# under the conditions described in the aforementioned license.  The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
#------------------------------------------------------------------------------

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig


# List of bundled toolkits.
_toolkits = [
    ('wx',  'enthought.pyface.toolkit_wx'),
    ('qt4', 'enthought.pyface.toolkit_qt4')
]

# The currently selected toolkit.
_toolkit = None


def toolkit():
    """ Returns the currently selected toolkit. """

    return _toolkit


def register_toolkit(name, package):
    """ Registers an external toolkit. """
    # Newly registered toolkits get priority over existing ones.
    _toolkits.insert(0, (name, package))


def select_toolkit(*args, **kw):
    """ Selects and initialises a low-level toolkit based on ETSConfig. """

    global _toolkit

    # Only one toolkit can be selected because of the monkey patching of class
    # dictionaries (and possibly for other reasons as well).
    if _toolkit is not None:
        return

    tkit_name = ETSConfig.toolkit

    if tkit_name == "":
        # Search the list of registered toolkits.
        toolkits = _toolkits
    else:
        for name, package in _toolkits:
            if tkit_name == name:
                break
        else:
            raise ValueError, "%s is not a registered toolkit" % tkit_name

        toolkits = [(name, package)]

    for name, package in toolkits:   
        root = package.split('.')[-1]

        try:
            module = __import__(package)
            _toolkit = getattr(module.pyface, root).toolkit
            _toolkit.name = name

            break
        except ImportError:
            pass
    else:
        raise ValueError, "Could not find any usable toolkits after trying %s" \
                % ', '.join([name for name, package in toolkits])

    # Initialise the toolkit.
    _toolkit.init_toolkit(*args, **kw)


class Toolkit(object):
    """ Abstract base class for toolkits. """

    # These must be overridden by the toolkit implementation.
    GUI = None
    Widget = None

    def init_toolkit(self, *args, **kw):
        """ Initialises the toolkit.

        This must be reimplemented.
        """

        raise NotImplementedError


def patch_toolkit(self):
    """ Make sure that an instance's class has been monkey patched for the
    selected toolkit.
    """

    # Make sure a toolkit has been selected.
    select_toolkit()

    _patch_class(self.__class__)


def _patch_class(cls):
    """ Make sure that a class has been monkey patched for the selected
    toolkit.
    """

    # Patch each superclass first.
    for sup in getattr(cls, '__bases__'):
        _patch_class(sup)

    # Now patch this class.
    if hasattr(cls, '__tko__'):
        tko_name = getattr(cls, '__tko__')
        tko = getattr(_toolkit, tko_name)

        for name, value in tko.__dict__.iteritems():
            # Don't patch in special methods.
            if not name.startswith('__'):
                setattr(cls, name, value)

        # No need to do it again.
        delattr(cls, '__tko__')
