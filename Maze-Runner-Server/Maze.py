from Cell import *


class Maze:
    width = 0
    height = 0
    maze = []

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.maze = [[Cell() for x in range(height)] for y in range(width)]
        for i in range(0, width):
            for j in range(0, height):
                temp = Cell()
                temp.position = Position(i, j)
                self.maze[i][j] = temp

    def getByPosition(self, position):
        return self.maze[position.x][position.y]
