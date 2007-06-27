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
import os


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
    """ Selects and initialises a low-level toolkit.  If a toolkit keyword
    argument is specified then it specifies the toolkit to use.  Otherwise
    sys.argv is searched for a '-toolkit' option.  Otherwise the value of the
    ETS_TOOLKIT environment variable is used if set.  Otherwise the list of
    of registered toolkits is tried in turn.
    """
    global _toolkit

    # Only one toolkit can be selected because of the monkey patching of class
    # dictionaries (and possibly for other reasons as well).  However that
    # doesn't stop explicit use of different toolkits providing they can share
    # event loops.
    if _toolkit is not None:
        return

    # See if a toolkit was specified on the command line by the user.  We
    # always do this so that it gets removed from the command line even if it
    # gets overridden by something else.
    tkit_argv = None

    try:
        idx = sys.argv.index('-toolkit')
    except ValueError:
        idx = -1

    if idx >= 1 and idx < len(sys.argv) - 1:
        tkit_argv = sys.argv[idx + 1]

        # Remove the flag from the command line.  Note that it always gets
        # removed even if it is not used.
        del sys.argv[idx:idx + 2]

    # See if a toolkit was specified programatically.
    tkit_name = kw.get('toolkit')

    # If not, see if it was specified on any command line.
    if tkit_name is None:
        tkit_name = tkit_argv

        # If not, see if the environment variable is specified.
        if tkit_name is None:
            tkit_name = os.environ.get('ETS_TOOLKIT')
    else:
        # Remove the argument.
        del kw['toolkit']

    if tkit_name is None:
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
