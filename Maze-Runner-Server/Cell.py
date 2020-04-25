class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:
    position = Position
    visited = False
    left = False
    right = False
    top = False
    bottom = False

    def connect(self, cell):
        if self.position.x < cell.position.x:
            self.right = True
            cell.left = True

        elif self.position.x > cell.position.x:
            self.left = True
            cell.right = True

        elif self.position.y < cell.position.y:
            self.bottom = True
            cell.top = True

        elif self.position.y > cell.position.y:
            self.top = True
            cell.bottom = True

    def getLeftNeighbor(self):
        if self.position.x == 0:
            return None
        return Position(self.position.x - 1, self.position.y)

    def getRightNeighbor(self, width):
        if self.position.x == width - 1:
            return None
        return Position(self.position.x + 1, self.position.y)

    def getTopNeighbor(self):
        if self.position.y == 0:
            return None
        return Position(self.position.x, self.position.y - 1)

    def getBottomNeighbor(self, height):
        if self.position.y == height - 1:
            return None
        return Position(self.position.x, self.position.y + 1)

    def getAllNeighbors(self, width, height):
        array = [
            self.getBottomNeighbor(height),
            self.getTopNeighbor(),
            self.getRightNeighbor(width),
            self.getLeftNeighbor()
        ]
        return list(filter(None, array))
