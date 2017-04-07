""" A basic toolkit implementation for use by specific toolkits

Writers of toolkit plugins are expected to provide a callable object which
takes a relative module path and an object name, separated by a colon.  The
assumption is that this is implemented by objects in sub-modules of the
toolkit, but plugin authors are free to use whatever methods they like.
"""

import os
import sys

from traits.api import HasTraits, List, ReadOnly, Str


class Toolkit(HasTraits):
    """ A basic toolkit implementation for use by specific toolkits.

    This implementation uses pathname mangling to find modules and objects in
    those modules.  If an object can't be found, the toolkit will return a
    class that raises NotImplementedError when it is instantiated.
    """

    #: The name of the toolkit
    toolkit = ReadOnly

    #: The packages to look in for widget implementations.
    package = List(Str)

    def __init__(self, toolkit, *packages, **traits):
        super(Toolkit, self).__init__(toolkit=toolkit, packages=list(packages),
                                      **traits)

    def __call__(self, name):
        """ Return the toolkit specific object with the given name.

        Parameters
        ----------
        name : str
            The name consists of the relative module path and the object name
            separated by a colon.
        """
        from importlib import import_module

        mname, oname = name.split(':')

        for package in self.packages:
            try:
                module = import_module('.' + mname, package)
            except ImportError as exc:
                # is the error while trying to import package mname or not?
                if all(part not in exc.args[0] for part in mname.split('.')):
                    # something else went wrong - let the exception be raised
                    raise

                # Ignore *ANY* errors unless a debug ENV variable is set.
                if 'ETS_DEBUG' in os.environ:
                    # Attempt to only skip errors in importing the backend modules.
                    # The idea here is that this only happens when the last entry in
                    # the traceback's stack frame mentions the toolkit in question.
                    import traceback
                    frames = traceback.extract_tb(sys.exc_traceback)
                    filename, lineno, function, text = frames[-1]
                    if not package in filename:
                        raise
            else:
                obj = getattr(module, oname, None)
                if obj is not None:
                    return obj

        toolkit = self.toolkit

        class Unimplemented(object):
            """ An unimplemented toolkit object

            This is returned if an object isn't implemented by the selected
            toolkit.  It raises an exception if it is ever instantiated.
            """

            def __init__(self, *args, **kwargs):
                msg = "the %s pyface backend doesn't implement %s"
                raise NotImplementedError(msg % (toolkit, name))

        return Unimplemented
