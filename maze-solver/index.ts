enum Cell {
  EMPTY = " ",
  BLOCKED = "X",
  START = "S",
  GOAL = "G",
  PATH = "#",
}

type MazeLocation = {
  row: number;
  column: number;
};

class Maze {
  private rows: number;
  private columns: number;
  private grid: Cell[][];
  start: MazeLocation;
  goal: MazeLocation;

  constructor(rows = 10, columns = 10, sparseness = 0.15) {
    this.rows = rows;
    this.columns = columns;
    this.start = { row: 0, column: 0 };
    this.goal = { row: rows - 1, column: columns - 1 };

    this.grid = this.createGrid();
    this.randomlyFillGrid(rows, columns, sparseness);
    this.grid[this.start.row][this.start.column] = Cell.START;
    this.grid[this.goal.row][this.goal.column] = Cell.GOAL;
  }

  private createGrid() {
    return Array.from({ length: this.rows }, () => Array(this.columns).fill(Cell.EMPTY));
  }

  private randomlyFillGrid(rows: number, columns: number, sparseness: number) {
    for (let row = 0; row < rows; row++) {
      for (let column = 0; column < columns; column++) {
        if (Math.random() < sparseness) {
          this.grid[row][column] = Cell.BLOCKED;
        }
      }
    }
  }

  private findNextPossibleLocations(ml: MazeLocation) {
    if (this.grid[ml.row][ml.column] === Cell.BLOCKED) {
      return;
    }

    const locations: MazeLocation[] = [];
    if (ml.row + 1 < this.rows && this.grid[ml.row + 1][ml.column] !== Cell.BLOCKED) {
      locations.push({ row: ml.row + 1, column: ml.column });
    }

    if (ml.row - 1 >= 0 && this.grid[ml.row - 1][ml.column] !== Cell.BLOCKED) {
      locations.push({ row: ml.row - 1, column: ml.column });
    }

    if (ml.column + 1 < this.columns && this.grid[ml.row][ml.column + 1] !== Cell.BLOCKED) {
      locations.push({ row: ml.row, column: ml.column + 1 });
    }

    if (ml.column - 1 >= 0 && this.grid[ml.row][ml.column - 1] !== Cell.BLOCKED) {
      locations.push({ row: ml.row, column: ml.column - 1 });
    }

    return locations;
  }

  private goalTest(ml: MazeLocation): boolean {
    return ml.row === this.goal.row && ml.column === this.goal.column;
  }

  drawPath(locations: MazeLocation[]) {
    for (const location of locations) {
      this.grid[location.row][location.column] = Cell.PATH;
    }
    this.grid[this.start.row][this.start.column] = Cell.START;
    this.grid[this.goal.row][this.goal.column] = Cell.GOAL;
  }

  solve() {
    // BFS always finds the shortest path since we check for possible paths in every step.
    const queue: MazeLocation[][] = [[this.start]]; // Holds lists of paths
    const visited: Set<string> = new Set([`${this.start.row},${this.start.column}`]);

    while (queue.length > 0) {
      const path = queue.shift()!;
      const currentLocation = path[path.length - 1];

      if (this.goalTest(currentLocation)) {
        this.drawPath(path);
        console.log(this.toString());
        return;
      }

      const nextLocations = this.findNextPossibleLocations(currentLocation);
      if (nextLocations) {
        for (const nextLocation of nextLocations) {
          const locationKey = `${nextLocation.row},${nextLocation.column}`;
          if (!visited.has(locationKey)) {
            // We create a new path for the queue extending the current one and
            // then append to queue to explore further
            visited.add(locationKey);
            queue.push([...path, nextLocation]);
          }
        }
      }
    }

    console.log("No solution");
  }

  toString(): string {
    return this.grid.map((row) => row.join("")).join("\n");
  }
}

function main() {
  const maze = new Maze(5, 30);
  maze.solve();
}

main();
