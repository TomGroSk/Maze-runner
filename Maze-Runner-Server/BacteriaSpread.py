from Cell import Position
from Converter import Converter
from Maze import Maze
from random import randint
from random import shuffle


class BacteriaSpread:
    @staticmethod
    def generate(x, y):
        mazeLayout = Maze(x, y)
        currentLayer = []
        nextLayer = []

        start = Position(randint(0, mazeLayout.width - 1), randint(0, mazeLayout.height - 1))

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

    @staticmethod
    def generateBooleanMaze(x, y):
        rawMaze = BacteriaSpread.generate(x, y)
        return Converter.toBoolArray(rawMaze)

    @staticmethod
    def generateEndPoint(mazeLayout, areaPercent):
        percentage = areaPercent / 100
        x, y = len(mazeLayout[0])-1, len(mazeLayout)-1         # size of maze - 1; upper range
        x_buffer = x - int(x * percentage)-1                   # % area where should not be end game point; lower range
        y_buffer = y - int(y * percentage)-1

        end_x = randint(x_buffer, x)
        end_y = randint(y_buffer, y)

        while mazeLayout[end_x][end_y]:
            end_x = randint(x_buffer, x)
            end_y = randint(y_buffer, y)

        return Position(end_x, end_y)






# BacteriaSpread.generateBooleanMaze(10, 10)