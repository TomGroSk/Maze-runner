class Position:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Cell:
    position = Position
    visited = False
    locked = False
    left = False
    right = False
    top = False
    bottom = False
    Locked = False

    def get_Locked(self):
        return self.locked

    def set_Locked(self, value):
        self.locked = value
        self.visited = value

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

    def disconnect(self, cell):
        if self.position.x < cell.position.x:
            self.right = False
            cell.left = False

        elif self.position.x > cell.position.x:
            self.left = False
            cell.right = False

        elif self.position.y < cell.position.y:
            self.bottom = False
            cell.top = False

        elif self.position.y > cell.position.y:
            self.top = False
            cell.bottom = False

    def getLeftNeighbor(self):
        if self.position.x == 0 or self.get_Locked():
            return None
        return Position(self.position.x - 1, self.position.y)

    def getRightNeighbor(self, width):
        if self.position.x == width - 1 or self.get_Locked():
            return None
        return Position(self.position.x + 1, self.position.y)

    def getTopNeighbor(self):
        if self.position.y == 0 or self.get_Locked():
            return None
        return Position(self.position.x, self.position.y - 1)

    def getBottomNeighbor(self, height):
        if self.position.y == height - 1 or self.get_Locked():
            return None
        return Position(self.position.x, self.position.y + 1)

    def getAllNeighbors(self, width, height):
        if self.locked: return []
        array = []
        if self.getBottomNeighbor(height): array.append(self.getBottomNeighbor(height))
        if self.getTopNeighbor(): array.append(self.getTopNeighbor())
        if self.getRightNeighbor(width): array.append(self.getRightNeighbor(width))
        if self.getLeftNeighbor(): array.append(self.getLeftNeighbor())
        return array
