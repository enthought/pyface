""" A basic toolkit implementation for use by specific toolkits

Writers of toolkit plugins are expected to provide a callable object which
takes a relative module path and an object name, separated by a colon.  The
assumption is that this is implemented by objects in sub-modules of the
toolkit, but plugin authors are free to use whatever methods they like.
"""

import os
import sys


class Unimplemented(object):
    """ An unimplemented toolkit object

    This is returned if an object isn't implemented by the selected
    toolkit.  It raises an exception if it is ever called, ie. used as a
    toolkit object factory.
    """

    def __init__(self, toolkit, name):
        self._toolkit = toolkit
        self._name = name

    def __call__(self, *args, **kwargs):
        msg = "the {} pyface backend doesn't implement {}"
        raise NotImplementedError(msg.format(self._toolkit, self._name))


class Toolkit(object):
    """ A basic toolkit implementation for use by specific toolkits

    This implementation uses pathname mangling to find modules and objects in
    those modules
    """

    def __init__(self, toolkit, package):
        self._toolkit = toolkit
        self._package = package

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

        be_obj = Unimplemented(self._toolkit, name)

        try:
            module = import_module('.' + mname, self._package)

            try:
                be_obj = getattr(module, oname)
            except AttributeError:
                pass
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
                if not self._package in filename:
                    raise

        return be_obj
