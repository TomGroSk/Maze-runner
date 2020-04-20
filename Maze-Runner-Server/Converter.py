from Cell import Position
from Maze import Maze
import sys

class Converter:
    def toBoolArray(self, maze: Maze):
        booleanArray = [[False for x in range(maze.height * 2)] for y in range(maze.width * 2)]
        for i in range(0, maze.width * 2, 2):
            for j in range(0, maze.height * 2, 2):
                if not maze.getByPosition(Position(i // 2, j // 2)).visited: continue

                if maze.getByPosition(Position(i // 2, j // 2)).bottom and maze.getByPosition(
                        Position(i // 2, j // 2)).right:
                    booleanArray[i][j] = True
                    booleanArray[i + 1][j] = True
                    booleanArray[i][j + 1] = True

                elif maze.getByPosition(Position(i // 2, j // 2)).bottom:
                    booleanArray[i][j] = True
                    booleanArray[i][j + 1] = True

                elif maze.getByPosition(Position(i // 2, j // 2)).right:
                    booleanArray[i][j] = True
                    booleanArray[i + 1][j] = True

                elif maze.getByPosition(Position(i // 2, j // 2)).get_Locked():
                    continue
                else:
                    booleanArray[i][j] = True

        for i in range(0, maze.width * 2):
            for j in range(0, maze.height * 2):
                if booleanArray[i][j]:
                    sys.stdout.write('x')
                else:
                    sys.stdout.write('.')
            print('')
        return booleanArray

