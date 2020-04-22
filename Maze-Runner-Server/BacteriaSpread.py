from Cell import Position
from Maze import Maze
from random import randint
from random import shuffle


class BacteriaSpread:
    @staticmethod
    def generate(x, y):
        mazeLayout = Maze(x, y)
        currentLayer = []
        nextLayer = []

        while True:
            start = Position(randint(0, mazeLayout.width - 1), randint(0, mazeLayout.height - 1))
            if not mazeLayout.getByPosition(start).locked:
                break

        mazeLayout.getByPosition(start).visited = True
        currentLayer.append(start)

        while len(currentLayer) > 0:
            for pos in currentLayer:
                neighbors = mazeLayout.getByPosition(pos).getAllNeighbors(mazeLayout.width, mazeLayout.height)

                for i in neighbors:
                    if not mazeLayout.getByPosition(i).visited:
                        mazeLayout.getByPosition(pos).connect(mazeLayout.getByPosition(i))
                        mazeLayout.getByPosition(i).visited = True
                        nextLayer.append(i)
            shuffle(nextLayer)
            currentLayer = nextLayer
            nextLayer = []

        return mazeLayout
