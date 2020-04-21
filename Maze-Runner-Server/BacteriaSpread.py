from Cell import Position
from Converter import Converter
from Maze import Maze
from random import randint
from random import shuffle


class BacteriaSpread:
    def generate(self, x, y):
        maze = Maze(x, y)
        currentLayer = []
        nextLayer = []

        while True:
            start = Position(randint(0, maze.width-1), randint(0, maze.height-1))
            if not maze.getByPosition(start).locked:
                break

        maze.getByPosition(start).visited = True
        currentLayer.append(start)

        while len(currentLayer) > 0:
            for pos in currentLayer:
                neighbors = maze.getByPosition(pos).getAllNeighbors(maze.width, maze.height)

                for i in neighbors:
                    if not maze.getByPosition(i).visited:
                        maze.getByPosition(pos).connect(maze.getByPosition(i))
                        maze.getByPosition(i).visited = True
                        nextLayer.append(i)
            shuffle(nextLayer)
            currentLayer = nextLayer
            nextLayer = []

        return maze
