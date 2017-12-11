from puzzle import Puzzle


class MNPuzzle(Puzzle):
    """
    An nxm puzzle, like the 15-puzzle, which may be solved, unsolved,
    or even unsolvable.
    """

    def __init__(self, from_grid, to_grid):
        """
        MNPuzzle in state from_grid, working towards
        state to_grid

        @param MNPuzzle self: this MNPuzzle
        @param tuple[tuple[str]] from_grid: current configuration
        @param tuple[tuple[str]] to_grid: solution configuration
        @rtype: None
        """
        # represent grid symbols with letters or numerals
        # represent the empty space with a "*"
        assert len(from_grid) > 0
        assert all([len(r) == len(from_grid[0]) for r in from_grid])
        assert all([len(r) == len(to_grid[0]) for r in to_grid])
        self.n, self.m = len(from_grid), len(from_grid[0])
        self.from_grid, self.to_grid = from_grid, to_grid

    # implement __eq__ and __str__
    # __repr__ is up to you

    def __eq__(self, other):
        """
        Return if MNPuzzle self is equivalent to other.

        @type self:  MNPuzzle
        @type other: MNPuzzle | Any
        @rtype: Bool

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> y = MNPuzzle(start_grid, target_grid)
        >>> x.__eq__(y)
        True
        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> start_grid = (("*", "2", "3"), ("1", "3", "4"))
        >>> y = MNPuzzle(start_grid, target_grid)
        >>> x.__eq__(y)
        False
        """
        return ((self.to_grid == other.to_grid) and
                (self.from_grid == other.from_grid) and
                type(self) == type(other))

    def __str__(self):
        """
        Return a human-readable string representation of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: str

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("2", "4", "3"), ("1", "*", "5"),("6", "7", "8"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> print(x)
        2 4 3
        1 * 5
        6 7 8
        """
        x = ''
        for i in self.from_grid:
            for j in range(len(i)):
                if j == len(i) - 1:
                    x += i[j]
                else:
                    x += i[j] + ' '  # Solve the problem in this.
            x += '\n'
        return x[0:len(x)-1]  # for removing the last blankline.

    # override extensions
    # legal extensions are configurations that can be reached by swapping one
    # symbol to the left, right, above, or below "*" with "*"

    def extensions(self):
        """
        Return list of legal extensions of MNPuzzle self.

        @type self: MNPuzzle
        @rtype: list[Puzzle]

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("2", "4", "3"), ("1", "*", "5"),("6", "7", "8"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> a = x.extensions()
        >>> print(a[0])
        2 4 3
        * 1 5
        6 7 8
        >>> print(a[1])
        2 4 3
        1 5 *
        6 7 8

        """
        extensions = []
        for tple in range(len(self.from_grid)): # interating over outer tuple
            for symbol in range(len(self.from_grid[tple])):  # over inner tuple
                if self.from_grid[tple][symbol] == '*':
                    if symbol == 0:
                        position1 = self.from_grid[tple][symbol+1]
                        position2 = self.from_grid[tple][symbol]
                        a = (position1, position2)
                        for i in self.from_grid[tple][2:]:
                            a += (i,)
                        lst = []
                        for item in self.from_grid:
                            if item != self.from_grid[tple]:
                                lst.append(item)
                            else :
                                lst.append(a)
                        x = tuple(lst)
                        extensions.append(MNPuzzle(x, self.to_grid))
                    elif symbol == len(self.from_grid[tple]) - 1:
                        position1 = self.from_grid[tple][symbol-1]
                        position2 = self.from_grid[tple][symbol]
                        a = (position2, position1)
                        tple1 = self.from_grid[tple][:symbol-1]
                        tple1 += a
                        lst = []
                        for item in self.from_grid:
                            if item != self.from_grid[tple]:
                                lst.append(item)
                            else:
                                lst.append(tple1)
                        x = tuple(lst)
                        extensions.append(MNPuzzle(x, self.to_grid))
                    else:
                        position1 = self.from_grid[tple][symbol+1]
                        position2 = self.from_grid[tple][symbol]
                        position3 = self.from_grid[tple][symbol-1]
                        tple1 = self.from_grid[tple][:symbol-1]
                        tple1 += (position2, position3)
                        tplea = self.from_grid[tple][symbol+1:]
                        tple1 += tplea
                        lst = []
                        for item in self.from_grid:
                            if item != self.from_grid[tple]:
                                lst.append(item)
                            else:
                                lst.append(tple1)
                        x = tuple(lst)
                        extensions.append(MNPuzzle(x, self.to_grid))
                        tple2 = self.from_grid[tple][:symbol]
                        tple2 += (position1, position2)
                        for i in self.from_grid[tple][symbol+2:]:
                            tple2 += (i,)
                        lst1 = []
                        for item in self.from_grid:
                            if item != self.from_grid[tple]:
                                lst1.append(item)
                            else:
                                lst1.append(tple2)
                        x = tuple(lst1)
                        extensions.append(MNPuzzle(x, self.to_grid))

        for tple in range(len(self.from_grid)):
            for symbol in range(len(self.from_grid[tple])):
                if self.from_grid[tple][symbol] == '*':
                    if tple == 0:
                        position1 = self.from_grid[tple][symbol]
                        position2 = self.from_grid[tple+1][symbol]
                        tple1 = self.from_grid[tple][:symbol]
                        tple1 += (position2,)
                        tple1 += self.from_grid[tple][symbol+1:]
                        tple2 = self.from_grid[tple+1][:symbol]
                        tple2 += (position1,)
                        tple2 += self.from_grid[tple+1][symbol+1:]
                        lst = []
                        lst.append(tple1)
                        lst.append(tple2)
                        for item in self.from_grid:
                            if item != self.from_grid[tple] and item !=  \
                                    self.from_grid[tple+1]:
                                lst.append(item)
                        x = tuple(lst)
                        extensions.append(MNPuzzle(x, self.to_grid))
                    elif tple == len(self.from_grid) - 1:
                        position1 = self.from_grid[tple][symbol]
                        position2 = self.from_grid[tple-1][symbol]
                        tple1 = self.from_grid[tple][:symbol]
                        tple1 += (position2,)
                        tple1 += self.from_grid[tple][symbol+1:]
                        tple2 = self.from_grid[tple-1][:symbol]
                        tple2 += (position1,)
                        tple2 += self.from_grid[tple-1][symbol+1:]
                        lst = []
                        for item in self.from_grid:
                            if item != self.from_grid[tple] and \
                                    (item != self.from_grid[tple-1]):
                                lst.append(item)
                        lst.append(tple2)
                        lst.append(tple1)
                        x = tuple(lst)
                        extensions.append(MNPuzzle(x, self.to_grid))
                    else:
                        position1 = self.from_grid[tple][symbol]
                        position2 = self.from_grid[tple+1][symbol]
                        position3 = self.from_grid[tple-1][symbol]
                        tple1 = self.from_grid[tple][:symbol]
                        tple1 += (position2,)
                        tple1 += self.from_grid[tple][symbol+1:]
                        tple2 = self.from_grid[tple+1][:symbol]
                        tple2 += (position1,)
                        tple2 += self.from_grid[tple+1][symbol+1:]
                        lst = []
                        for item in range(len(self.from_grid)):
                            if item != tple and item != tple + 1:
                                lst.append(self.from_grid[item])
                            elif item == tple:
                                lst.append(tple1)
                            else:
                                lst.append(tple2)
                        x = tuple(lst)
                        extensions.append(MNPuzzle(x, self.to_grid))
                        tple3 = self.from_grid[tple-1][:symbol]
                        tple3 += (position1,)
                        tple3 += self.from_grid[tple-1][symbol+1:]
                        tple4 = self.from_grid[tple][:symbol]
                        tple4 += (position3,)
                        tple4 += self.from_grid[tple][symbol+1:]
                        lst1 = []
                        for item in range(len(self.from_grid)):
                            if item != tple and item != tple - 1:
                                lst1.append(self.from_grid[item])
                            elif item == tple:
                                lst1.append(tple4)
                            else:
                                lst1.append(tple3)
                        x = tuple(lst1)
                        extensions.append(MNPuzzle(x, self.to_grid))

        return extensions
    # sorry for the long code.

    def is_solved(self):
        """
        Return whether MNPuzzle self is solved.

        @type self: MNPuzzle
        @rtype: Bool | Any

        >>> target_grid = (("1", "2", "3"), ("4", "5", "*"))
        >>> start_grid = (("*", "2", "3"), ("1", "4", "5"))
        >>> x = MNPuzzle(start_grid, target_grid)
        >>> x.is_solved()
        False

        """
        return self.from_grid == self.to_grid


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    target_grid = (("1", "2", "3"), ("4", "5", "*"))
    start_grid = (("*", "2", "3"), ("1", "4", "5"))
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    start = time()
    solution = breadth_first_solve(MNPuzzle(start_grid, target_grid))
    end = time()
    print("BFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
    start = time()
    solution = depth_first_solve((MNPuzzle(start_grid, target_grid)))
    end = time()
    print("DFS solved: \n\n{} \n\nin {} seconds".format(
        solution, end - start))
