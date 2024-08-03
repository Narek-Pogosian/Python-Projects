import random

from enum import Enum
from typing import List, NamedTuple


class Cell(str, Enum):
    EMPTY = ""
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(
        self,
        rows=10,
        columns=10,
        start=MazeLocation(0, 0),
        goal=MazeLocation(9, 9),
        sparseness=0.2,
    ):
        self._rows = rows
        self._columns = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal

        self._grid: List[List[Cell]] = [
            [Cell.PATH for _ in range(columns)] for _ in range(rows)
        ]
        self._randomly_fill(rows, columns, sparseness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output


def main():
    maze = Maze()
    print(maze)


if __name__ == "__main__":
    main()
