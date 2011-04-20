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
    # Handle a degenerate case for which the logic below will fail (because
    # prev_item will not be set).
    if len(items) < 2:
        return items

    # Build a set of pairs representing the graph.
    item_map = dict((item.id, item) for item in items if item.id)
    pairs = []
    prev_item = None
    for item in items:
        # Attempt to use 'before' and 'after' to make pairs.
        new_pairs = []
        if hasattr(item, 'before') and item.before:
            parent, child = item, item_map.get(item.before)
            if child:
                new_pairs.append((parent, child))
            else:
                logger.warning('No item with ID %r', item.before)
        if hasattr(item, 'after') and item.after:
            parent, child = item_map.get(item.after), item
            if parent:
                new_pairs.append((parent, child))
            else:
                logger.warning('No item with ID %r', item.after)

        # If we have any pairs, use them. Otherwise, use the previous unmatched
        # item as a parent, if possible.
        if new_pairs:
            pairs.extend(new_pairs)
        else:
            if prev_item:
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
