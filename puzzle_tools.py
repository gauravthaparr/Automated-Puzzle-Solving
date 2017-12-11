"""
Some functions for working with puzzles
"""
from puzzle import Puzzle
from collections import deque
# set higher recursion limit
# which is needed in PuzzleNode.__str__
# uncomment the next two lines on a unix platform, say CDF
# import resource
# resource.setrlimit(resource.RLIMIT_STACK, (2**29, -1))
import sys

sys.setrecursionlimit(10 ** 6)

# *** HELPER FUNCTIONS FOR BREADTH_FIRST_SOLVE AND DEPTH_FIRST_SOLVE ***


def helper_sol(puzzle, lst):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing a
    solution, with each child containing an extension of the puzzle in its
    parent. Return None if this is not possible.

    @type puzzle : puzzle.py
    @type lst: list | deque
    @rtype: PuzzleNode

    """
    visit = set()
    lst.append(PuzzleNode(puzzle))
    flag = False
    sol = None
    while lst and not flag:
        if isinstance(lst, deque):
            croot = lst.popleft()
        else:
            croot = lst.pop()
        current = croot.puzzle
        if str(current) not in visit:
            if current.is_solved():  # if already solved.
                # turn current_root into a leaf
                croot.children = []
                sol = path_ret(croot) # croot is basically the current root.
                flag = True
            else:
                visit.add(str(current))
                extensions = current.extensions()
                ex_nodes = [PuzzleNode(extension, parent=croot) for
                            extension in extensions]
                croot.children = ex_nodes
                lst.extend(ex_nodes)
    return sol


def path_ret(leaf):
    """
    Returns the path between the root of the tree and leaf.

    @type leaf: PuzzleNode
    @rtype: PuzzleNode

    >>> node = PuzzleNode()
    >>> node == path_ret(node)
    True
    >>> node2 = PuzzleNode(parent=node)
    >>> node3 = PuzzleNode(parent=node2)
    >>> node2.children = [node3]
    >>> node == path_ret(node2)
    True
    """
    if leaf.parent is None:
        return leaf
    else:
        parent = leaf.parent  # iteration starts in the tree.
        parent.children = [leaf]
        return path_ret(parent)

# *** HELPER FUNCTIONS OVER ***


def depth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child containing an extension of the puzzle
    in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None

    >>> from word_ladder_puzzle import WordLadderPuzzle
    >>> x = WordLadderPuzzle('cost','cave',{'cast'})
    >>> sol = depth_first_solve(x)
    >>> print(sol)
    None
    >>> x = WordLadderPuzzle('cost','cave',{'cast','case','cave'})
    >>> sol = depth_first_solve(x)
    >>> print(sol)
    cost -> cave
    <BLANKLINE>
    cast -> cave
    <BLANKLINE>
    case -> cave
    <BLANKLINE>
    cave -> cave
    <BLANKLINE>
    <BLANKLINE>

    """
    return helper_sol(puzzle, [])


def breadth_first_solve(puzzle):
    """
    Return a path from PuzzleNode(puzzle) to a PuzzleNode containing
    a solution, with each child PuzzleNode containing an extension
    of the puzzle in its parent.  Return None if this is not possible.

    @type puzzle: Puzzle
    @rtype: PuzzleNode | None

    >>> from word_ladder_puzzle import WordLadderPuzzle
    >>> x = WordLadderPuzzle('cost','cave',{'cast'})
    >>> sol = breadth_first_solve(x)
    >>> print(sol)
    None
    >>> x = WordLadderPuzzle('cost','cave',{'cast','case','cave'})
    >>> sol = breadth_first_solve(x)
    >>> print(sol)
    cost -> cave
    <BLANKLINE>
    cast -> cave
    <BLANKLINE>
    case -> cave
    <BLANKLINE>
    cave -> cave
    <BLANKLINE>
    <BLANKLINE>

    """
    # The blank line above is due to the return.
    return helper_sol(puzzle, deque())

# Class PuzzleNode helps build trees of PuzzleNodes that have
# an arbitrary number of children, and a parent.


class PuzzleNode:
    """
    A Puzzle configuration that refers to other configurations that it
    can be extended to.
    """

    def __init__(self, puzzle=None, children=None, parent=None):
        """
        Create a new puzzle node self with configuration puzzle.

        @type self: PuzzleNode
        @type puzzle: Puzzle | None
        @type children: list[PuzzleNode]
        @type parent: PuzzleNode | None
        @rtype: None
        """
        self.puzzle, self.parent = puzzle, parent
        if children is None:
            self.children = []
        else:
            self.children = children[:]

    def __eq__(self, other):
        """
        Return whether PuzzleNode self is equivalent to other

        @type self: PuzzleNode
        @type other: PuzzleNode | Any
        @rtype: bool

        >>> from word_ladder_puzzle import WordLadderPuzzle
        >>> pn1 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "no", "oo"}))
        >>> pn2 = PuzzleNode(WordLadderPuzzle("on", "no", {"on", "oo", "no"}))
        >>> pn3 = PuzzleNode(WordLadderPuzzle("no", "on", {"on", "no", "oo"}))
        >>> pn1.__eq__(pn2)
        True
        >>> pn1.__eq__(pn3)
        False
        """
        return (type(self) == type(other) and
                self.puzzle == other.puzzle and
                all([x in self.children for x in other.children]) and
                all([x in other.children for x in self.children]))

    def __str__(self):
        """
        Return a human-readable string representing PuzzleNode self.

        # doctest not feasible.
        """
        return "{}\n\n{}".format(self.puzzle,
                                 "\n".join([str(x) for x in self.children]))
