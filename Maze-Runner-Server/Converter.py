from Cell import Position
from Maze import Maze


class Converter:

    @staticmethod
    def toBoolArray(maze: Maze):
        booleanArray = [[True for x in range(maze.height * 2+1)] for y in range(maze.width * 2+1)]

        for i in range(1, maze.width * 2, 2):
            for j in range(1, maze.height * 2, 2):
                if not maze.getByPosition(Position(i // 2, j // 2)).visited:
                    continue

                if maze.getByPosition(Position(i // 2, j // 2)).bottom and maze.getByPosition(
                        Position(i // 2, j // 2)).right:
                    booleanArray[i][j] = False
                    booleanArray[i + 1][j] = False
                    booleanArray[i][j + 1] = False

                elif maze.getByPosition(Position(i // 2, j // 2)).bottom:
                    booleanArray[i][j] = False
                    booleanArray[i][j + 1] = False

                elif maze.getByPosition(Position(i // 2, j // 2)).right:
                    booleanArray[i][j] = False
                    booleanArray[i + 1][j] = False
                else:
                    booleanArray[i][j] = False

        return booleanArray
