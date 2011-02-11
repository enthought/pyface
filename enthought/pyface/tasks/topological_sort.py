# Standard library imports.
from collections import defaultdict
import logging

# Logging.
logger = logging.getLogger(__name__)


def before_after_sort(items):
    """ Sort a sequence of items with 'before', 'after', and 'id' attributes.
        
    The sort is topological. If an item does not specify a 'before' or 'after',
    it is placed after the preceding item.

    Any inconsistencies that are found (including cycles) are logged.
    """
    # Build a set of pairs representing the graph.
    item_map = dict((item.id, item) for item in items)
    pairs = []
    prev_item = None
    for item in items:
        # Attempt to use 'before' or 'after' to make a pair.
        if item.before:
            parent, child = item, item_map.get(item.before)
            if not child:
                logger.warning('No item with ID %r', item.before)
        elif item.after:
            parent, child = item_map.get(item.after), item
            if not parent:
                logger.warning('No item with ID %r', item.after)
        else:
            parent = child = None

        # If we have a pair, use it. Otherwise, use the previous item as a
        # parent, if possible
        if parent and child:
            pairs.append((parent, child))
        elif prev_item:
            pairs.append((prev_item, item))
        prev_item = item

    # Now perform the actual sort.
    result, has_cycle = topological_sort(pairs)
    if has_cycle:
        logger.warning('Cycle in sequence %r', items)
    return result


def topological_sort(pairs):
    """ Topologically sort a list of (parent, child) pairs.

    Returns a tuple containing the list of elements sorted in dependency order
    (parent to child order), if possible, and a boolean indicating whether the
    graph contains cycles.

    A simple algorithm due to Kahn, in which vertices are chosen from the graph
    in the same order as the eventual topological sort, is used.
    """
    # Represent the graph in dictionary form.
    graph = defaultdict(list)
    num_parents = defaultdict(int)
    for parent, child in pairs:
        graph[parent].append(child)
        num_parents[child] += 1

    # Begin with the parent-less items.
    result = [ item for item in graph.keys() if num_parents[item] == 0 ]
    
    # Descend through graph, removing parents as we go.
    for parent in result:
        if graph.has_key(parent):
            for child in graph[parent]:
                num_parents[child] -= 1
                if num_parents[child] == 0:
                    result.append(child)
            del graph[parent]

    # If there's a cycle, just throw in whatever is left over.
    has_cycle = bool(graph)
    if has_cycle:
        result.append(graph.keys())
    return result, has_cycle
