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

        self._grid: List[List[Cell]] = [[Cell.PATH for _ in range(columns)] for _ in range(rows)]
        self._randomly_fill(rows, columns, sparseness)
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        """Randomly fill blocks in maze, amount based on sparseness (0 - 1)"""
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    def goal_test(self, ml: MazeLocation):
        """Check if current location is at the goal"""
        return ml == self.goal
    
    def find_next_possible_locations(self, ml: MazeLocation) -> List[MazeLocation]:
        """Return wich locations are available out of the top, right, bottom, left locations."""
        if self._grid[ml.row][ml.column] == Cell.BLOCKED:
            return
        
        locations: List[MazeLocation] = []
        if ml.row + 1 < self._rows and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row + 1, ml.column))

        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))

        if ml.column + 1 < self._columns and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column + 1))

        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
            
        return locations

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output


def find_solution(maze: Maze):
    """
    Use DFS to find solution, go through each path as far as 
    possible before backtrack.
    """
    print(maze.find_next_possible_locations(MazeLocation(2,3)))


def main():
    maze = Maze()
    find_solution(maze)


if __name__ == "__main__":
    main()
