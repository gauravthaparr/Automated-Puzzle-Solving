from puzzle import Puzzle


class WordLadderPuzzle(Puzzle):
    """
    A word-ladder puzzle that may be solved, unsolved, or even unsolvable.
    """

    def __init__(self, from_word, to_word, ws):
        """
        Create a new word-ladder puzzle with the aim of stepping
        from from_word to to_word using words in ws, changing one
        character at each step.

        @type from_word: str
        @type to_word: str
        @type ws: set[str]
        @rtype: None
        """
        (self._from_word, self._to_word, self._word_set) = (from_word,
                                                            to_word, ws)
        # set of characters to use for 1-character changes
        self._chars = "abcdefghijklmnopqrstuvwxyz"

        # implement __eq__ and __str__
        # __repr__ is up to you

    def __eq__(self, other):
        """
        Return if WordLadderPuzzle self is equivalent to other.

        @type self: WordLadderPuzzle
        @type other: WordLadderPuzzle | Any
        @rtype: Bool

        >>> x = WordLadderPuzzle('cost','cave',{'cast','case','cave'})
        >>> y = WordLadderPuzzle('cost','save',{'cast','case','cave'})
        >>> x.__eq__(y)
        False

        """
        return (type(self) == type(other) and
                (self._from_word == other._from_word) and
                (self._to_word == other._to_word) and
                (self._word_set == other._word_set))

    def __str__(self):
        """
        Return a human-readable string representation of WordLadderPuzzle self.

        @type: WordLadderPuzzle
        @rtype: str

        >>> x = WordLadderPuzzle('cost','cave',{'cast','case','cave'})
        >>> print(x)
        cost -> cave

        """
        return '{0} -> {1}'.format(self._from_word, self._to_word)

    # override extensions
    # legal extensions are WordLadderPuzzles that have a from_word that can
    # be reached from this one by changing a single letter to one of those
    # in self._chars

    def extensions(self):
        """
        Return list of extensions of WordLadderPuzzle self.

        @param self:
        @type self:
        @rtype: list

        >>> x = WordLadderPuzzle('cost','cave',{'cast','case','cave'})
        >>> a = x.extensions()
        >>> for i in a: print(i)
        cast -> cave

        """
        wset = self._word_set
        final = []
        for x in self._chars:
            for index in range(len(self._from_word)):
                from_word = self._from_word
                from_word = from_word[:index]+x+from_word[index+1:]
                final.append(from_word)
        final_list = []
        for x in final:
            if x in wset:
                final_list.append(WordLadderPuzzle(x, self._to_word, wset))

        return final_list

        # override is_solved
        # this WordLadderPuzzle is solved when _from_word is the same as
        # _to_word

    def is_solved(self):
        """
        Return whether WordLadderPuzzle self is solved.

        @type self: WordLadderPuzzle
        @rtype: Bool

        >>> x = WordLadderPuzzle('cost','cave',{'cast','case','cave'})
        >>> x.is_solved()
        False

        """
        return self._from_word == self._to_word

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    from puzzle_tools import breadth_first_solve, depth_first_solve
    from time import time
    with open("words", "r") as words:
        word_set = set(words.read().split())
    w = WordLadderPuzzle("same", "cost", word_set)
    start = time()
    sol = breadth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using breadth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
    start = time()
    sol = depth_first_solve(w)
    end = time()
    print("Solving word ladder from same->cost")
    print("...using depth-first-search")
    print("Solutions: {} took {} seconds.".format(sol, end - start))
