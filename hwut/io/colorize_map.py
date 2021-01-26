from   hwut.common            import color

import sys
import random

def do(Text, Ratio):
    assert type(Text) == list
    size_y = len(Text)
    size_x = len(Text[0]) - 1
    assert all(len(line) == size_x for line in Text)

    mountain_map = PositionColorMap(Ratio, size_x, size_y)

    txt = []
    for y, line in enumerate(Text):
        previous_color = None
        # Assume that the last letter in the line in newline, which is not colored.
        for x, letter in enumerate(line[:-1]):
            if (x, y) in mountain_map: c = color().Back.RED
            else:                      c = color().Back.GREEN
            if c != previous_color:
                txt.append(color().Style.RESET_ALL)
                txt.append(c)
            txt.append(letter)
        txt.append(color().Style.RESET_ALL)
        txt.append("\n")

    return "".join(txt)

class PositionColorMap(set):
    def __init__(self, Ratio, SizeX, SizeY):
        self.__size_x         = SizeX
        self.__size_y         = SizeY
        self.__candidate_list = [ (x,0) for x in range(self.__size_x) ]

        surface         = self.__size_x * self.__size_y
        covered_place_n = surface * Ratio
        result          = set()
        print "#covered_place_n:", covered_place_n
        for i in range(int(covered_place_n)):
            index  = random.randint(0, len(self.__candidate_list)-1)
            choice = self.__candidate_list[index]
            del self.__candidate_list[index]

            assert choice not in self
            self.add(choice)
            self.__candidates_find(choice)

    def __candidates_find(self, Position):
        X, Y = Position
        if Y < self.__size_y - 1: self.__candidates_add((X,   Y+1))
        if X > 0:                 self.__candidates_add((X-1, Y))
        if X < self.__size_x - 1: self.__candidates_add((X+1, Y))

    def __candidates_add(self, Position):
        if   Position in self: return
        elif Position in self.__candidate_list: return
        self.__candidate_list.append(Position)

    def get_string(self):
        covered_n = len(self)
        txt = ["coverage: %i/%i;\n" % (len(self), self.__size_x * self.__size_y)]
        for y in reversed(range(self.__size_y)):
            txt.append("[%2i] " % y)
            txt.extend(self.get_character(x, y) for x in range(self.__size_x))
            txt.append("\n")
        return "".join(txt)

    def get_character(self, X, Y):
        if   (X, Y) not in self:         return " "
        elif Y == 0 or (X, Y+1) in self: return "#"
        else:                            return "+"

if __name__ == "__main__":
    for i in xrange(0, 11):
        ratio = 0.1 * i
        print PositionColorMap(ratio, 120, 7).get_string()

