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

# Standard library imports.
import sys

# Enthought library imports.
from enthought.etsconfig.api import ETSConfig


# This is set to the root part of the module path for the selected backend.
_toolkit_backend = None


def _init_toolkit():
    """ Initialise the current toolkit. """

    # Toolkits to check for if none is explicitly specified.
    known_toolkits = ('wx', 'qt4')

    # Get the toolkit.
    toolkit = ETSConfig.toolkit

    if toolkit:
        toolkits = (toolkit, )
    else:
        toolkits = known_toolkits

    for tk in toolkits:
        # Try and import the toolkit's pyface backend just to see if it is
        # there.
        be = 'enthought.pyface.ui.' + tk

        try:
            __import__(be)
            break
        except ImportError:
            pass
    else:
        if toolkit:
            raise ImportError, "unable to import a pyface backend for the %s toolkit" % toolkit
        else:
            raise ImportError, "unable to import a pyface backend for any of the %s toolkits" % ", ".join(known_toolkits)

    # In case we have just decided on a toolkit, tell everybody else.
    ETSConfig.toolkit = tk

    # Save the imported toolkit module.
    global _toolkit_backend

    _toolkit_backend = be + '.'


# Do this once then disappear.
_init_toolkit()
del _init_toolkit


def toolkit_object(name):
    """ Return the toolkit specific object with the given name.  The name
    consists of the relative module path and the object name separated by a
    colon.
    """

    mname, oname = name.split(':')
    be_mname = _toolkit_backend + mname

    class Unimplemented(object):
        """ This is returned if an object isn't implemented by the selected
        toolkit.  It raises an exception if it is ever instantiated.
        """

        def __init__(self, *args, **kwargs):
            raise NotImplementedError("the %s pyface backend doesn't implement %s" % (ETSConfig.toolkit, oname))

    be_obj = Unimplemented

    try:
        __import__(be_mname)

        try:
            be_obj = getattr(sys.modules[be_mname], oname)
        except AttributeError:
            pass
    except ImportError:
        pass

    return be_obj


###############################################################################
# The rest of this file is legacy stuff which will be removed when all the
# previously ported Qt support has been refactored.
###############################################################################

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
    #Widget = None

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
