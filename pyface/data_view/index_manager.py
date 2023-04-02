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
Index Managers
==============

This module provides a number of classes for efficiently managing the
mapping between different ways of representing indices.  To do so, each
index manager provides an intermediate, opaque index object that is
suitable for use in these situations and is guaranteed to have a long
enough life that it will not change or be garbage collected while a C++
object has a reference to it.

The wx DataView classes expect to be given an integer id value that is
stable and can be used to return the parent reference id.

And Qt's ModelView system expects to be given a pointer to an object
that is long-lived (in particular, it will not be garbage-collected
during the lifetime of a QModelIndex) and which can be used to find
the parent object of the current object.

The default representation of an index from the point of view of the
data view infrastructure is a sequence of integers, giving the index at
each level of the hierarchy.  DataViewModel classes can then use these
indices to identify objects in the underlying data model.

There are three main classes defined in the module: AbstractIndexManager,
IntIndexManager, and TupleIndexManager.

AbstractIndexManager
    An ABC that defines the API

IntIndexManager
    An efficient index manager for non-hierarchical data, such as
    lists, tables and 2D arrays.

TupleIndexManager
    An index manager that handles non-hierarchical data while trying
    to be fast and memory efficient.

The two concrete subclasses should be sufficient for most cases, but advanced
users may create their own if for some reason the provided managers do not
work well for a particular situation.  Developers who implement this API
need to be mindful of the requirements on the lifetime and identity
constraints required by the various toolkit APIs.

"""

from abc import abstractmethod

from traits.api import ABCHasStrictTraits, Dict, Int, Tuple


#: The singular root object for all index managers.
Root = ()


class AbstractIndexManager(ABCHasStrictTraits):
    """ Abstract base class for index managers.
    """

    @abstractmethod
    def create_index(self, parent, row):
        """ Given a parent index and a row number, create an index.

        The internal structure of the index should not matter to
        consuming code.  However obejcts returned from this method
        should persist until the reset method is called.

        Parameters
        ----------
        parent : index object
            The parent index object.
        row : int
            The position of the resuling index in the parent's children.

        Returns
        -------
        index : index object
            The resulting opaque index object.

        Raises
        ------
        IndexError
            Negative row values raise an IndexError exception.
        RuntimeError
            If asked to create a persistent index for a parent and row
            where that is not possible, a RuntimeError will be raised.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_parent_and_row(self, index):
        """ Given an index object, return the parent index and row.

        Parameters
        ----------
        index : index object
            The opaque index object.

        Returns
        -------
        parent : index object
            The parent index object.
        row : int
            The position of the resuling index in the parent's children.

        Raises
        ------
        IndexError
            If the Root object is passed as the index, this method will
            raise an IndexError, as it has no parent.
        """
        raise NotImplementedError()

    def from_sequence(self, indices):
        """ Given a sequence of indices, return the index object.

        The default implementation starts at the root and repeatedly calls
        create_index() to find the index at each level, returning the final
        value.

        Parameters
        ----------
        indices : sequence of int
            The row location at each level of the hierarchy.

        Returns
        -------
        index : index object
            The persistent index object associated with this sequence.

        Raises
        ------
        RuntimeError
            If asked to create a persistent index for a sequence of indices
            where that is not possible, a RuntimeError will be raised.
        """
        index = Root
        for row in indices:
            index = self.create_index(index, row)
        return index

    def to_sequence(self, index):
        """ Given an index, return the corresponding sequence of row values.

        The default implementation repeatedly calls get_parent_and_row()
        to walk up the hierarchy and push the row values into the start
        of the sequence.

        Parameters
        ----------
        index : index object
            The opaque index object.

        Returns
        -------
        sequence : tuple of int
            The row location at each level of the hierarchy.
        """
        result = ()
        while index != Root:
            index, row = self.get_parent_and_row(index)
            result = (row,) + result
        return result

    @abstractmethod
    def from_id(self, id):
        """ Given an integer id, return the corresponding index.

        Parameters
        ----------
        id : int
            An integer object id value.

        Returns
        -------
        index : index object
            The persistent index object associated with this id.
        """
        raise NotImplementedError()

    @abstractmethod
    def id(self, index):
        """ Given an index, return the corresponding id.

        Parameters
        ----------
        index : index object
            The persistent index object.

        Returns
        -------
        id : int
            The associated integer object id value.
        """
        raise NotImplementedError()

    def reset(self):
        """ Reset any caches and other state.

        Resettable traits in subclasses are indicated by having
        ``can_reset=True`` metadata.  This is provided to allow
        toolkit code to clear caches to prevent memory leaks when
        working with very large tables.

        Care should be taken when calling this method, as Qt may
        crash if a QModelIndex is referencing an index that no
        longer has a reference in a cache.

        For some IndexManagers, particularly for those which are flat
        or static, reset() may do nothing.
        """
        resettable_traits = self.trait_names(can_reset=True)
        self.reset_traits(resettable_traits)


class IntIndexManager(AbstractIndexManager):
    """ Efficient IndexManager for non-hierarchical indexes.

    This is a simple index manager for flat data structures.  The
    index values returned are either the Root, or simple integers
    that indicate the position of the index as a child of the root.

    While it cannot handle nested data, this index manager can
    operate without having to perform any caching, and so is very
    efficient.
    """

    def create_index(self, parent, row):
        """ Given a parent index and a row number, create an index.

        This should only ever be called with Root as the parent.

        Parameters
        ----------
        parent : index object
            The parent index object.
        row : non-negative int
            The position of the resulting index in the parent's children.

        Returns
        -------
        index : index object
            The resulting opaque index object.

        Raises
        ------
        IndexError
            Negative row values raise an IndexError exception.
        RuntimeError
            If the parent is not the Root, a RuntimeError will be raised
        """
        if row < 0:
            raise IndexError("Row must be non-negative.  Got {}".format(row))
        if parent != Root:
            raise RuntimeError(
                "{} cannot create persistent index value for {}.".format(
                    self.__class__.__name__,
                    (parent, row)
                )
            )
        return row

    def get_parent_and_row(self, index):
        """ Given an index object, return the parent index and row.

        Parameters
        ----------
        index : index object
            The opaque index object.

        Returns
        -------
        parent : index object
            The parent index object.
        row : int
            The position of the resuling index in the parent's children.

        Raises
        ------
        IndexError
            If the Root object is passed as the index, this method will
            raise an IndexError, as it has no parent.
        """
        if index == Root:
            raise IndexError("Root index has no parent.")
        return Root, int(index)

    def from_id(self, id):
        """ Given an integer id, return the corresponding index.

        Parameters
        ----------
        id : int
            An integer object id value.

        Returns
        -------
        index : index object
            The persistent index object associated with this id.
        """
        if id == 0:
            return Root
        return id - 1

    def id(self, index):
        """ Given an index, return the corresponding id.

        Parameters
        ----------
        index : index object
            The persistent index object.

        Returns
        -------
        id : int
            The associated integer object id value.
        """
        if index == Root:
            return 0
        return index + 1


class TupleIndexManager(AbstractIndexManager):

    #: A dictionary that maps tuples to the canonical version of the tuple.
    _cache = Dict(Tuple, Tuple, {Root: Root}, can_reset=True)

    #: A dictionary that maps ids to the canonical version of the tuple.
    _id_cache = Dict(Int, Tuple, {0: Root}, can_reset=True)

    def create_index(self, parent, row):
        """ Given a parent index and a row number, create an index.

        Parameters
        ----------
        parent : index object
            The parent index object.
        row : non-negative int
            The position of the resulting index in the parent's children.

        Returns
        -------
        index : index object
            The resulting opaque index object.

        Raises
        ------
        IndexError
            Negative row values raise an IndexError exception.
        """
        if row < 0:
            raise IndexError("Row must be non-negative.  Got {}".format(row))

        index = (parent, row)
        canonical_index = self._cache.setdefault(index, index)
        self._id_cache[self.id(canonical_index)] = canonical_index
        return canonical_index

    def get_parent_and_row(self, index):
        """ Given an index object, return the parent index and row.

        Parameters
        ----------
        index : index object
            The opaque index object.

        Returns
        -------
        parent : index object
            The parent index object.
        row : int
            The position of the resuling index in the parent's children.

        Raises
        ------
        IndexError
            If the Root object is passed as the index, this method will
            raise an IndexError, as it has no parent.
        """
        if index == Root:
            raise IndexError("Root index has no parent.")
        return index

    def from_id(self, id):
        """ Given an integer id, return the corresponding index.

        Parameters
        ----------
        id : int
            An integer object id value.

        Returns
        -------
        index : index object
            The persistent index object associated with this id.
        """
        return self._id_cache[id]

    def id(self, index):
        """ Given an index, return the corresponding id.

        Parameters
        ----------
        index : index object
            The persistent index object.

        Returns
        -------
        id : int
            The associated integer object id value.
        """
        if index == Root:
            return 0
        canonical_index = self._cache.setdefault(index, index)
        return id(canonical_index)
