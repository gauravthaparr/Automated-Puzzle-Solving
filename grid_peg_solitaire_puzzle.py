from puzzle import Puzzle
from copy import deepcopy


class GridPegSolitairePuzzle(Puzzle):
    """
    Snapshot of peg solitaire on a rectangular grid. May be solved,
    unsolved, or even unsolvable.
    """

    def __init__(self, marker, marker_set):
        """
        Create a new GridPegSolitairePuzzle self with
        marker indicating pegs, spaces, and unused
        and marker_set indicating allowed markers.

        @type marker: list[list[str]]
        @type marker_set: set[str]
                          "#" for unused, "*" for peg, "." for empty
        """
        assert isinstance(marker, list)
        assert len(marker) > 0
        assert all([len(x) == len(marker[0]) for x in marker[1:]])
        assert all([all(x in marker_set for x in row) for row in marker])
        assert all([x == "*" or x == "." or x == "#" for x in marker_set])
        self._marker, self._marker_set = marker, marker_set

    # implement __eq__, __str__ methods
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return if GridPegSolitairePuzzle self is equivalent to other.

        @type self:  GridPegSolitairePuzzle
        @type other: GridPegSolitairePuzzle | Any
        @rtype: Bool

        >>> grid = [["#", "*", "*", "*", "*"],["*", "*", "*", "*", "*"],\
        ["*", "*", "*", "*", "*"],["*", "*", ".", "*", "*"],\
        ["*", "*", "#", "*", "*"]]
        >>> x = GridPegSolitairePuzzle(grid,['#','*','.'])
        >>> grid1 = [["#", "*", "*", "*", "*"],["*", "*", "*", "*", "*"],\
        ["*", "*", "*", "*", "*"],["*", "*", ".", "*", "*"],\
        ["*", "*", "#", "*", "*"]]
        >>> y = GridPegSolitairePuzzle(grid1,['#','*','.'])
        >>> x.__eq__(y)
        True

        """
        return ((self._marker == other._marker) and
                (self._marker_set == other._marker_set) and
                (type(self) == type(other)))

    def __str__(self):
        """
        Return a human-readable string representation of GridPegSolitairePuzzle
        self.

        @type self: GridPegSolitairePuzzle
        @rtype: str

        >>> grid = [["#", "*", "*", "*", "*"],["*", "*", "*", "*", "*"],\
        ["*", "*", "*", "*", "*"],["*", "*", ".", "*", "*"],\
        ["*", "*", "#", "*", "*"]]
        >>> g = GridPegSolitairePuzzle(grid, ['#','*','.'])
        >>> print(g)
        #****
        *****
        *****
        **.**
        **#**

        """
        s = ''
        new_copy = self._marker.copy()
        for i in new_copy:
            s += "".join(i) + '\n'
        s = s.rstrip('\n')
        return s

    # override extensions
    # legal extensions consist of all configurations that can be reached by
    # making a single jump from this configuration

    def extensions(self):
        """
        Return list of extensions of GridPegSolitairePuzzle self.

        @type self: GridPegSolitairePuzzle
        @rtype: list[puzzle]

        >>> grid = [["*", ".", "*", "*", "*"], ["*", "*", "*", "*", "*"],\
        ["*", "*", "*", "*", "*"], ["*", "*", ".", "*", "*"],\
        ["*", "*", "*", "*", "*"]]
        >>> x = GridPegSolitairePuzzle(grid,{'*','#','.'})
        >>> a = x.extensions()
        >>> y = []
        *.***
        *****
        *****
        ***..
        *****

        """
        dct = {}
        for i in range(len(self._marker[0])):
            for j in range(len(self._marker)):
                dct[(i, j)] = self._marker[j][i]
        if str(self).count("*") == 1 or str(self).count(".") == 0:
            # checking for '*' and if the next character is '.'
            return [_ for _ in []]
        else:
            extensions = []
            index_i = 0
            index_j = 0
            for character in self._marker:
                index_j += 1
                if "." in character:
                    index_j -= 1
                    index_i += character.index(".")
                    break
            row = deepcopy(self._marker[index_j])
            col = deepcopy(self._marker[index_i])
            size1 = len([x for x in row if x != "#"])
            size2 = len([x for x in col if x != "#"])

            for item in dct:
                if (item[0] < (size1 - 2) and
                    dct[item] == "." and
                    dct[item[0] + 1, item[1]] == "*" and
                        dct[item[0] + 2, item[1]] == "*"):
                    lst_copy = deepcopy(self._marker)
                    lst_copy[item[1]][item[0]] = "*"
                    lst_copy[item[1]][item[0] + 1] = "."
                    lst_copy[item[1]][item[0] + 2] = "."
                    solution = GridPegSolitairePuzzle(lst_copy, {"*", ".", "#"})
                    if not (solution in extensions):
                        extensions.append(solution)

                if (item[0] > 1 and
                    dct[item] == "." and
                    dct[item[0] - 1, item[1]] == "*" and
                        dct[item[0] - 2, item[1]] == "*"):
                    lst_copy = deepcopy(self._marker)
                    lst_copy[item[1]][item[0]] = "*"
                    lst_copy[item[1]][item[0] - 1] = "."
                    lst_copy[item[1]][item[0] - 2] = "."
                    solution = GridPegSolitairePuzzle(lst_copy, {"*", ".", "#"})
                    if not (solution in extensions):
                        extensions.append(solution)

                if (item[1] < (size2 - 2) and
                    dct[item] == "." and
                    dct[item[0], item[1] + 1] == "*" and
                        dct[item[0], item[1] + 2] == "*"):
                    lst_copy = deepcopy(self._marker)
                    lst_copy[item[1]][item[0]] = "*"
                    lst_copy[item[1] + 1][item[0]] = "."
                    lst_copy[item[1] + 2][item[0]] = "."
                    solution = GridPegSolitairePuzzle(lst_copy, {"*", ".", "#"})
                    if not (solution in extensions):
                        extensions.append(solution)

                if (item[1] > 1 and
                    dct[item] == "." and
                    dct[item[0], item[1] - 1] == "*" and
                        dct[item[0], item[1] - 2] == "*"):
                    lst_copy = deepcopy(self._marker)
                    lst_copy[item[1]][item[0]] = "*"
                    lst_copy[item[1] - 1][item[0]] = "."
                    lst_copy[item[1] - 2][item[0]] = "."
                    solution = GridPegSolitairePuzzle(lst_copy, {"*", ".", "#"})
                    if not (solution in extensions):
                        extensions.append(solution)
            return extensions

    # override is_solved
    # A configuration is solved when there is exactly one "*" left

    def is_solved(self):
        """
        Return whether GridPegSolitairePuzzle self is solved.

        @type self : GridPegSolitairePuzzle
        @rtype: Bool

         >>> grid = [["#", ".", ".", ".", "."],[".", ".", ".", ".", "."],\
         [".", ".", ".", ".", "."],[".", ".", ".", ".", "."],\
         [".", ".", ".", ".", "*"]]
        >>> g = GridPegSolitairePuzzle(grid, ['#','*','.'])
        >>> g.is_solved()
        True
        """
        count = 0
        for i in self._marker:
            for j in i:
                if j == '*':
                    count += 1
        if count == 1:
            return True
        return False


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    from puzzle_tools import depth_first_solve

    grid = [["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", "*", "*", "*"],
            ["*", "*", ".", "*", "*"],
            ["*", "*", "*", "*", "*"]]
    gpsp = GridPegSolitairePuzzle(grid, {"*", ".", "#"})
    import time

    start = time.time()
    solution = depth_first_solve(gpsp)
    end = time.time()
    print("Solved 5x5 peg solitaire in {} seconds.".format(end - start))
    print("Using depth-first: \n{}".format(solution))
