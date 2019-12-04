## board.py ##
## Author: Carson Foster ##

## Purpose: define a class for the Hawlweigh board.  ##
from operator import add

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y    
    @classmethod
    def fromTuple(self, t):
        x, y = t
        return Point(x, y)
    def __str__(self):
        stringPoint = "({}, {})".format(self.x, self.y)
        return stringPoint
    def __add__(self, other):
        try:
            return Point(self.x + other.x, self.y + other.y)
        except:
            x, y = other
            return Point(self.x + x, self.y + y)
    def __eq__(self, other):
        try:
            return self.x == other.x and self.y == other.y
        except:
            x, y = other
            return self.x == x and self.y == y
    def __ne__(self, other):
        return not self.__eq__(other)
    def __sub__(self, other):
        try:
            return Point(self.x - other.x, self.y - other.y)
        except:
            x, y = other
            return Point(self.x - x, self.y - y)

class Line():
    def __init__(self, p1, p2):
        if "Point" not in str(type(p1)):
            x1, y1 = p1
            self.p1 = Point(x1, y1)
            x2, y2 = p2
            self.p2 = Point(x2, y2)
        else:
            self.p1 = p1
            self.p2 = p2
    def __eq__(self, other):
        try:
            return (self.p1 == other.p1 and self.p2 == other.p2) or (self.p1 == other.p2 and self.p2 == other.p1)
        except:
            p1, p2 = other
            return (self.p1 == p1 and self.p2 == p2) or (self.p1 == p2 and self.p2 == p1)
    def __ne__(self, other):
        return not self.__eq__(other)
    def __str__(self):
        line = "A" + str(self.p1) + "B" + str(self.p2)
        line = "{}\n".format("-" * len(line)) + line
        return line
    def __contains__(self, item):
        miny = min(self.p1.y, self.p2.y)
        maxy = max(self.p1.y, self.p2.y)
        minx = min(self.p1.x, self.p2.x)
        maxx = max(self.p1.x, self.p2.x)
        if self.orientation() == "v":
            try:
                if item.x == self.p1.x:
                    if item.y > miny and item.y < maxy:
                        return True
                return False
            except:
                if item[0] == self.p1.x:
                    if item[1] > miny and item[1] < maxy:
                        return True
                return False
        m = float((self.p2.y - self.p1.y)) / float((self.p2.x - self.p1.x))
        b = self.p1.y - (m * self.p1.x)
        try:
            if item.y == (m * item.x) + b:
                if miny == maxy:
                    if item.y == miny and item.x > minx and item.x < maxx:
                        return True
                if minx == maxx:
                        if item.x == minx and item.y > miny and item.y < maxy:
                            return True
                if item.y > miny and item.y < maxy and item.x > minx and item.x < maxx:
                    return True
        except:
            if item[1] == (m * item[0]) + b:
                if miny == maxy:
                    if item[1] == miny and item[0] > minx and item[0] < maxx:
                        return True
                if minx == maxx:
                        if item[0] == minx and item[1] > miny and item[1] < maxy:
                            return True
                if item[1] > miny and item[1] < maxy and item[0] > minx and item[0] < maxx:
                    return True
        return False
    def orientation(self):
        if (self.p1.x == self.p2.x):
            return "v"
        elif (self.p1.y == self.p2.y):
            return "h"
        else:
            return "d"

class Board():
    def __init__(self, spots, walls):
        self.spots = spots # 9 x 9 2D array
        # [ [...], 0
                                  # [...], 1
                                  # [...], 2
                                  # [...], 3
                                  # [...], 4
                                  # [...], 5
                                  # [...], 6
                                  # [...], 7
                                  # [...] ] 8
                                  # oneD is vertical (positive), twoD is horizontal
        self.walls = walls # array of lines
        # B = black token, W = white token
    @classmethod
    def blankBoard(self):
        spots = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(" ")
            spots.append(row)
        spots[0][4] = "W" # spots[y][x]
        spots[8][4] = "B"
        walls = []
        return Board(spots, walls)
    def copy(self):
        return Board([row[:] for row in self.spots], self.walls[:])
    def winner(self):
        dests = set([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (0, 0)])
        for dest in dests:
            if self.spots[dest[1]][dest[0]] == "B":
                return "B"
        dests = set([(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (0, 8)])
        for dest in dests:
            if self.spots[dest[1]][dest[0]] == "W":
                return "W"
        return None
    def isLegalMove(self, oneD, twoD, letter, n=0, a=0, b=[]):
        if n > 5 or a > 5:
            return False
        if oneD >= 9 or oneD < 0 or twoD >= 9 or twoD < 0:
            return False
        oneD, twoD = twoD, oneD # call isLegalMove(x, y, letter)
        letter = letter.upper()
        # check for blank
        if self.spots[oneD][twoD] != " " and self.spots[oneD][twoD] != "":
            return False
        # get position
        for i in self.spots:
            for j in i:
                ba = j
                if ba == letter:
                    pos = (i.index(j), self.spots.index(i))
                    break
            if ba == letter:
                break
        # check for wall in the way
        x, y = twoD, oneD
        lines = {(x, y - 1):(((x - 1, y), (x + 1,y)), ((x,y), (x + 2, y))), (x, y + 1):(((x - 1,y + 1),(x + 1,y + 1)), ((x,y + 1),(x + 2,y + 1))), (x - 1, y): (((x,y - 1),(x,y + 1)), ((x,y),(x,y + 2))), (x + 1, y):(((x + 1,y - 1),(x + 1,y + 1)), ((x + 1,y),(x + 1,y + 2)))}
        for possiblePos in list(lines.keys()):
            if possiblePos == pos:
                for line in lines[pos]:
                    for wall in self.walls:
                        if wall == line:
                            b.append("wall")
                            return False
        # right angle or straight check
        move = (x, y)
        adds = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        for op in adds:
            if tuple(map(add, pos, op)) == move:
                return True
        # jump one space
        if letter == "B":
            nLetter = "W"
        else:
            nLetter = "B"
        adds = [(0, -2), (0, 2), (2, 0), (-2, 0)]
        tmp = False
        for op in adds:
            if tuple(map(add, pos, op)) == move:
                tmp = True
                break
        if tmp:
            adds = [(0, -1), (0, 1), (1, 0), (-1, 0)]
            dupe = self.copy()
            for op in adds:
                dims = list(map(add, pos, op))
                try:
                    if self.spots[dims[1]][dims[0]] == nLetter:
                        dupe.spots[dims[1]][dims[0]] = " "
                        if dupe.isLegalMove(dims[0], dims[1], letter, n, a + 1):
                            dupe.spots[dims[1]][dims[0]] = letter
                            dupe.spots[pos[1]][pos[0]] = " "
                            move2 = list(map(add, (dims[0], dims[1]), op))
                            if tuple(move2) == move and dupe.isLegalMove(move2[0], move2[1], letter, n, a + 1):
                                return True
                except:
                    continue
                            
        # jump adjacent space
        # test if straight jump possible -> not legal
        # replace oLetter and see if that is legal
        oPos = (0, 0)
        for i in self.spots:
            for j in i:
                ba = j
                if ba == nLetter:
                    oPos = (i.index(j), self.spots.index(i))
                    break
            if ba == nLetter:
                break
        adds = [(0, -1), (0, 1), (1, 0), (-1, 0)]
        direction = (0, 0)
        for op in adds:
            if tuple(map(add, op, pos)) == oPos:
                direction = op
                break
        if direction == (0, 0):
            return False
        jump = tuple(map(add, oPos, direction))
        cdef = []
        if self.isLegalMove(jump[0], jump[1], letter, n + 1, 0, cdef) or not "wall" in cdef:
            return False
        dupe = self.copy()
        dupe.spots[oPos[1]][oPos[0]] = letter
        if dupe.isLegalMove(x, y, letter, n, a + 1):
            return True
        return False
    def legalMoves(self, letter):
        legal = []
        for i in range(len(self.spots)):
            for j in range(len(self.spots[i])):
                if self.isLegalMove(j, i, letter):
                    legal.append((j, i))
        return legal
    def dijkstra(self, start, end, graph):
        to_visit = {start}
        visited = set()
        distance = {start: 0}
        parents = dict()

        while to_visit:
            current = min([(distance[node], node) for node in to_visit])[1]
            if current == end:
                break
            to_visit.discard(current)
            visited.add(current)
            edges = graph[current]
            neighbours = set(edges).difference(visited)
            for neighbour in neighbours:
                neighbour_distance = distance[current] + 1
                if neighbour_distance < distance.get(neighbour, float('inf')):
                    distance[neighbour] = neighbour_distance
                    parents[neighbour] = current
                    to_visit.add(neighbour)
        if end not in parents:
            return None
        cursor = end
        path = []
        while cursor:
            path.append(cursor)
            cursor = parents.get(cursor)
        return list(reversed(path))
    def getPath(self, letter):
        if letter == "B":
            nLetter = "W"
            dests = set([(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (0, 0)])
        else:
            nLetter = "B"
            dests = set([(1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (0, 8)])
        oPos = (0, 0)
        for i in range(len(self.spots)):
            for j in range(len(self.spots[i])):
                if self.spots[i][j] == letter:
                    pos = (j, i)
                if self.spots[i][j] == nLetter:
                    oPos = (j, i)
        graph = dict()
        for i in range(len(self.spots)):
            for j in range(len(self.spots[i])):
                dupe = self.copy()
                dupe.spots[oPos[1]][oPos[0]] = " " ################## legal moves not right
                dupe.spots[pos[1]][pos[0]] = " "
                dupe.spots[i][j] = letter
                graph[(j, i)] = dupe.legalMoves(letter)
        shortestPathCount = float('inf')
        shortestPath = []
        for dest in dests:
            path = self.dijkstra(pos, dest, graph)
            if path == None:
                continue
            if len(path) < shortestPathCount:
                shortestPathCount = len(path)
                shortestPath = path
        if shortestPath == []:
            return None
        return shortestPath

    def isLegalWall(self, line, letter):
        try:
            a = line.p1.x
        except:
            p1, p2 = line
            line = Line(p1, p2)
        if letter.upper() == "B":
            nLetter = "W"
        else:
            nLetter = "B"
        if line.orientation() == "v":
            if abs(line.p1.y - line.p2.y) != 2:
                return False
        elif line.orientation() == "h":
            if abs(line.p1.x - line.p2.x) != 2:
                return False
        else:
            return False
        if abs(line.p1.x - line.p2.x) == 2 and abs(line.p1.y - line.p2.y) == 2:
            return False
        if line.p1.x >= 10 or line.p1.x < 0 or line.p1.y >= 10 or line.p1.y < 0 or line.p2.x >= 10 or line.p2.x < 0 or line.p2.y >= 10 or line.p2.y < 0:
            return False
        if type(line.p1.x) != type(1) or type(line.p1.y) != type(1) or type(line.p2.x) != type(1) or type(line.p2.y) != type(1):
            return False
        center = ((line.p1.x + line.p2.x) / 2, (line.p1.y + line.p2.y) / 2)
        for wall in self.walls:
            wCenter = ((wall.p1.x + wall.p2.x) / 2, (wall.p1.y + wall.p2.y) / 2)
            if center in wall:
                return False
            if (line.p1 == wCenter or line.p2 == wCenter) and wall.orientation() == line.orientation():
                return False

        dupe = self.copy()
        dupe.walls.append(line)
        a = dupe.getPath(nLetter)
        if a == None: #############
            return False
        return True

#print((4, 4) in Line((3, 4), (5, 4)))
#board = Board.blankBoard()
#board.walls.append(Line((3, 4), (5, 4)))
#print(board.isLegalWall(Line((4, 4), (4, 6)), "W"))
#board.spots[0][4] = " "
#board.spots[8][4] = " "
#board.spots[3][4] = "W"
#board.spots[4][4] = "B"
#print(board.isLegalMove(4, 5, "W"))
#board.walls.append(Line((4, 7), (6,7)))
#board.walls.append(Line((4, 7), (4, 9)))
#i = 0
#while i < 4:
#    board.walls.append(Line((i, 1), (i + 2, 1)))
#    i += 2
#i = 6
#while i + 2 <= 10:
#    board.walls.append(Line((i, 1), (i + 2, 1)))
#    i += 2
#print(board.isLegalWall(Line((4, 1), (6, 1)), "B"))
#print(board.legalMoves("W"))
#print(board.legalMoves("B"))
#print((3, 7) in Line((3, 6), (3, 2)))
#print(board.getPath("B"))