import random

from enum import Enum
from collections import deque
from typing import List, NamedTuple


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "#"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(
        self,
        rows=10,
        columns=10,
        sparseness=0.15,
    ):
        self._rows = rows
        self._columns = columns
        self.start = MazeLocation(0, 0)
        self.goal = MazeLocation(rows-1, columns-1)

        self._grid: List[List[Cell]] = [[Cell.EMPTY for _ in range(columns)] for _ in range(rows)]
        self._randomly_fill(rows, columns, sparseness)
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        """Randomly fill blocks in maze, amount based on sparseness (0 - 1)"""
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

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

    def goal_test(self, ml: MazeLocation):
        """ Check if current location is at the goal"""
        return ml == self.goal
    
    def draw_path(self, locations: List[MazeLocation]):
        """Draws the locations in the maze grid as #"""
        for location in locations:
            self._grid[location.row][location.column] = Cell.PATH
            self._grid[self.start.row][self.start.column] = Cell.START
            self._grid[self.goal.row][self.goal.column] = Cell.GOAL

        print(self)

    def solve(self) -> None:
        """Tries to find a solution using BFS, prints out the path if it exists else a message"""
        queue = deque([[self.start]])
        visited = set([self.start])

        while queue:
            path = queue.popleft()
            current_location = path[-1]

            if self.goal_test(current_location):
                self.draw_path(path)

            for next_location in self.find_next_possible_locations(current_location):
                if next_location not in visited:
                    visited.add(next_location)
                    new_path = list(path)
                    new_path.append(next_location)
                    queue.append(new_path)

        print("No solution")

    def __str__(self) -> str:
        output = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output


def main():
    maze = Maze(rows=5, columns=30)
    maze.solve()

if __name__ == "__main__":
    main()
