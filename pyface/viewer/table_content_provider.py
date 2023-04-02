# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

""" Abstract base class for table content providers. """


from .content_provider import ContentProvider


class TableContentProvider(ContentProvider):
    """ Abstract base class for table content providers.

    Table content providers are used by (surprise, surprise) table viewers!

    """

    # This class currently does not specialize the base class in any way.
    # It is here to (hopefully) make the APIs for the viewer, content and label
    # provider classes more consistent.  In particular, if you are building a
    # table viewer you sub-class 'TableContentProvider' and
    # 'TableLabelProvider'.  For a tree viewer you sub-class
    # 'TreeContentProvider' and 'TreeLabelProvider'  instead of some
    # combination of the specific and generic viewer classes as in JFace.
    pass
