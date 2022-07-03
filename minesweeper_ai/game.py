import random
from random import randint, choice

class Game:
    def __init__(self, n, m, bombs, seed=None):
        self.__seed = seed
        self.bombsCount = bombs
        self.status = 0
        self.board = [["#" for x in range(n)] for y in range(m)]
        self.bombs = []
        if seed != None:
            self.__generateBombs()

    def __generateBombs(self, x=None, y=None):
        if self.__seed != None:
            random.seed(self.__seed)
        while (len(self.bombs) < self.bombsCount):
            r_y = random.randint(0, len(self.board[0]) - 1)
            r_x = random.randint(0, len(self.board) - 1)
            if self.__seed == None:
                if r_x != x and r_y != y and (r_x, r_y) not in self.bombs:
                    self.bombs.append((r_x, r_y))
            else:
                if (r_x, r_y) not in self.bombs:
                    self.bombs.append((r_x, r_y))

    def checkWin(self):
        if sum(row.count('#') for row in self.board) == self.bombsCount:
            self.status = 1

    def getUnopenedCells(self):
        moves = []
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board[0])):
                if self.board[i][j] == "#":
                    moves.append((i, j))
        return moves

    def getBoardConfig(self, bombsList):
        self.bombs = bombsList
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.openCell(i, j)
        return self.board

    def openCell(self, x, y):
        if len(self.bombs) == 0:
            self.__generateBombs(x, y)
        if (x, y) in self.bombs:
            self.status = -1
            self.board[x][y] = "B"
        else:
            # Logic of openning
            self.__recOpen(x, y)
            self.checkWin()

    def __recOpen(self, x, y):
        adj = [(a, b) for a, b in
               [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1), (x - 1, y - 1), (x + 1, y + 1), (x + 1, y - 1),
                (x - 1, y + 1)]]
        counter = 0
        safeCells = []
        for test in adj:
            if test[0] < len(self.board) and test[1] < len(self.board[0]) and test[0] >= 0 and test[1] >= 0:
                if test in self.bombs:
                    counter += 1
                else:
                    safeCells.append(test)
        if counter == 0:
            self.board[x][y] = "_"
        else:
            self.board[x][y] = str(counter)
        if self.board[x][y] == "_":
            for cell in safeCells:
                if self.board[cell[0]][cell[1]] == "#":
                    self.__recOpen(cell[0], cell[1])