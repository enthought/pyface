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
# Author: Prabhu Ramachandran <prabhu_r@users.sf.net>
# Description: <Enthought pyface package component>
#------------------------------------------------------------------------------
"""This module adds a fix for wx.py's introspect module.

In order to do code-completion, the function
`introspect.getAttributeName` accesses all the attributes of the
current object.  This causes severe problems for modules like tvtk
which depend on lazy importing.  The original introspect module also
has severe problems with large Numeric arrays because it calls str()
on the Numeric object in order to find its methods.

This file defines a fixed function that works fine with lazy objects
and large Numeric arrays.  This fixed function is injected into the
introspect module.
"""

# Import introspect.
from wx.py import introspect

import types

# The fixed function.
def getAttributeNames(object, includeMagic=1, includeSingle=1,
                      includeDouble=1):
    """Return list of unique attributes, including inherited, for object."""
    attributes = []
    dict = {}
    if not introspect.hasattrAlwaysReturnsTrue(object):
        # Add some attributes that don't always get picked up.
        special_attrs = ['__bases__', '__class__', '__dict__', '__name__',
                         'func_closure', 'func_code', 'func_defaults',
                         'func_dict', 'func_doc', 'func_globals', 'func_name']
        attributes += [attr for attr in special_attrs \
                       if hasattr(object, attr)]
    # For objects that have traits, get all the trait names since
    # these do not show up in dir(object).
    if hasattr(object, 'trait_names'):
        try:
            attributes += object.trait_names()
        except TypeError:
            pass

    if includeMagic:
        try: attributes += object._getAttributeNames()
        except: pass
    # Get all attribute names.
    attrdict = getAllAttributeNames(object)
    # Store the object's dir.
    object_dir = dir(object)
    for (obj_type_name, technique, count), attrlist in attrdict.items():
        # This complexity is necessary to avoid accessing all the
        # attributes of the object.  This is very handy for objects
        # whose attributes are lazily evaluated.
        if type(object).__name__ == obj_type_name and technique == 'dir':
            attributes += attrlist
        else:
            attributes += [attr for attr in attrlist \
                           if attr not in object_dir and \
                           hasattr(object, attr)]

    # Remove duplicates from the attribute list.
    for item in attributes:
        dict[item] = None
    attributes = dict.keys()
    # new-style swig wrappings can result in non-string attributes
    # e.g. ITK http://www.itk.org/
    attributes = [attribute for attribute in attributes \
                  if isinstance(attribute, basestring)]
    attributes.sort(lambda x, y: cmp(x.upper(), y.upper()))
    if not includeSingle:
        attributes = filter(lambda item: item[0]!='_' \
                            or item[1]=='_', attributes)
    if not includeDouble:
        attributes = filter(lambda item: item[:2]!='__', attributes)
    return attributes


# Replace introspect's version with ours.
introspect.getAttributeNames = getAttributeNames

# This is also a modified version of the function which does not use
# str(object).
def getAllAttributeNames(object):
    """Return dict of all attributes, including inherited, for an object.

    Recursively walk through a class and all base classes.
    """
    attrdict = {}  # (object, technique, count): [list of attributes]
    # !!!
    # Do Not use hasattr() as a test anywhere in this function,
    # because it is unreliable with remote objects: xmlrpc, soap, etc.
    # They always return true for hasattr().
    # !!!
    try:
        # This could(?) fail if the type is poorly defined without
        # even a name.
        key = type(object).__name__
    except:
        key = 'anonymous'
    # Wake up sleepy objects - a hack for ZODB objects in "ghost" state.
    wakeupcall = dir(object)
    del wakeupcall
    # Get attributes available through the normal convention.
    attributes = dir(object)
    attrdict[(key, 'dir', len(attributes))] = attributes
    # Get attributes from the object's dictionary, if it has one.
    try:
        attributes = object.__dict__.keys()
        attributes.sort()
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        attrdict[(key, '__dict__', len(attributes))] = attributes
    # For a class instance, get the attributes for the class.
    try:
        klass = object.__class__
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        if klass is object:
            # Break a circular reference. This happens with extension
            # classes.
            pass
        else:
            attrdict.update(getAllAttributeNames(klass))
    # Also get attributes from any and all parent classes.
    try:
        bases = object.__bases__
    except:  # Must catch all because object might have __getattr__.
        pass
    else:
        if isinstance(bases, types.TupleType):
            for base in bases:
                if type(base) is types.TypeType:
                    # Break a circular reference. Happens in Python 2.2.
                    pass
                else:
                    attrdict.update(getAllAttributeNames(base))
    return attrdict
