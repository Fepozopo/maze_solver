from tkinter import Tk, BOTH, Canvas
from time import sleep
import random


class Window:
    def __init__(self, width, height):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.width = width
        self.height = height
        self.canvas = Canvas(self.__root, width=self.width, height=self.height)
        self.canvas.pack()
        self.running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        """
        Call the root widget's update_idletasks() and update() methods to redraw the canvas.
        """
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        """
        Set the data member we created to track the "running" state of the window to True.
        Next, it should call self.redraw() over and over as long as the running state remains True.
        """
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        '''
        Set the running state to False.
        '''
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)


class Cell:
    def __init__(self, x1, y1, x2, y2, win=None):
        """
        Initialize a new cell with walls on all sides
        Args:
            x1: Left x coordinate
            y1: Top y coordinate
            x2: Right x coordinate
            y2: Bottom y coordinate
            win: Window instance for drawing
        """
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win
        self.visited = False
        
        # By default, all walls exist
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
    def draw(self):
        """
        Draw the cell's walls based on their existence state
        """
        # Create lines for each existing wall. Draw a black line if the wall exists, otherwise draw a white line
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "white")
            
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "white")
            
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "white")
            
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
        else:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "white")

    def draw_move(self, to_cell, undo=False):
        """
        Draw a line from the center of this cell to the center of another cell.
        
        Args:
            to_cell: The destination Cell instance
            undo: Boolean indicating if this is a backtrack move
        """
        # Calculate center points of both cells
        from_x = (self._x1 + self._x2) // 2
        from_y = (self._y1 + self._y2) // 2
        
        to_x = (to_cell._x1 + to_cell._x2) // 2
        to_y = (to_cell._y1 + to_cell._y2) // 2
        
        # Create the line between cell centers
        line = Line(
            Point(from_x, from_y),
            Point(to_x, to_y)
        )
        
        # Draw in red for forward moves, gray for backtracking
        color = "gray" if undo else "red"
        self._win.draw_line(line, color)



class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        """
        Initialize the maze with a grid of cells
        
        Args:
            x1: Starting x coordinate of the maze
            y1: Starting y coordinate of the maze
            num_rows: Number of rows in the maze
            num_cols: Number of columns in the maze
            cell_size_x: Width of each cell
            cell_size_y: Height of each cell
            win: Window instance for drawing
        """
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self.seed = seed

        # Set the random seed
        if self.seed is not None:
            random.seed(self.seed)
        
        # Initialize the grid of cells
        self.cells = []
        self._create_cells()
        self._break_entrance_and_exit()

        # Break the walls to create the maze
        self._break_walls_r(0, 0)
        
    def _create_cells(self):
        """
        Create a 2D grid of cells and draw them
        """
        # Create the columns
        for i in range(self._num_cols):
            col = []
            # Create the rows
            for j in range(self._num_rows):
                col.append(None)  # Initialize with None, will be replaced in _draw_cell
            self.cells.append(col)
        
        # Now create and draw each cell
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)
                
    def _draw_cell(self, i, j):
        """
        Calculate the position and create a new cell at the specified grid position
        
        Args:
            i: Column index
            j: Row index
        """
        # Calculate the actual pixel coordinates for this cell
        x1 = self._x1 + (i * self._cell_size_x)
        y1 = self._y1 + (j * self._cell_size_y)
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        
        # Create the cell
        cell = Cell(x1, y1, x2, y2, self._win)
        self.cells[i][j] = cell
        
        # Draw and animate the cell
        if self._win is not None:
            cell.draw()
            self._animate() # Animate the drawing
        
    def _animate(self):
        """
        Animate the maze drawing with a small delay between frames
        """
        if self._win is not None:
            self._win.redraw()
            sleep(0.01)

    def _break_entrance_and_exit(self):
        """
        Remove walls to create entrance at top-left and exit at bottom-right
        """
        # Break the top wall of the entrance (top-left cell)
        self.entrance_cell = self.cells[0][0]
        self.entrance_cell.has_top_wall = False
        if self._win is not None:
            self.entrance_cell.draw()
        
        # Break the bottom wall of the exit (bottom-right cell)
        self.exit_cell = self.cells[self._num_cols - 1][self._num_rows - 1]
        self.exit_cell.has_bottom_wall = False
        if self._win is not None:
            self.exit_cell.draw()

    def _break_walls_r(self, i, j):
        """
        A depth-first traversal through the cells, breaking down walls as it goes.
        Uses an iterative approach to prevent stack overflow for large mazes.
        """
        # Mark the current cell as visited
        self.cells[i][j].visited = True

        # In an infinite loop...
        while True:
            # List to hold unvisited neighbors
            to_visit = []

            # Check all adjacent cells
            # Left neighbor
            if i > 0 and not self.cells[i - 1][j].visited:
                to_visit.append(("left", i - 1, j))
            # Right neighbor
            if i < self._num_cols - 1 and not self.cells[i + 1][j].visited:
                to_visit.append(("right", i + 1, j))
            # Top neighbor
            if j > 0 and not self.cells[i][j - 1].visited:
                to_visit.append(("up", i, j - 1))
            # Bottom neighbor
            if j < self._num_rows - 1 and not self.cells[i][j + 1].visited:
                to_visit.append(("down", i, j + 1))

            # If no unvisited neighbors, we're done with this cell
            if len(to_visit) == 0:
                if self._win is not None:
                    self.cells[i][j].draw()
                    self._animate()
                return
            
            # Choose a random direction and get its coordinates
            direction, next_i, next_j = random.choice(to_visit)
            
            # Break walls between current cell and chosen cell
            if direction == "left":
                self.cells[i][j].has_left_wall = False
                self.cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                self.cells[i][j].has_right_wall = False
                self.cells[next_i][next_j].has_left_wall = False
            elif direction == "up":
                self.cells[i][j].has_top_wall = False
                self.cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                self.cells[i][j].has_bottom_wall = False
                self.cells[next_i][next_j].has_top_wall = False
                
            # Draw the current cell
            if self._win is not None:
                self.cells[i][j].draw()
                self.cells[next_i][next_j].draw()
                self._animate()
                
            # Recursively visit the next cell
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        """
        Reset the visited state of all cells
        """
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self.cells[i][j].visited = False

    def solve(self):
        """
        Solve the maze starting from the entrance.
        Returns True if a solution is found, False otherwise.
        """
        self._reset_cells_visited()
    
        # Initialize stack with starting position
        stack = [(0, 0, None)]  # (i, j, previous_cell)
        path = []  # Keep track of solution path
        
        while stack:
            i, j, previous = stack.pop()
            current_cell = self.cells[i][j]
            
            if not current_cell.visited:
                # Mark current cell as visited
                current_cell.visited = True
                
                # Draw move from previous cell if it exists
                if previous is not None:
                    previous.draw_move(current_cell)
                    path.append((previous, current_cell))
                
                # Check if we reached the exit
                if i == self._num_cols - 1 and j == self._num_rows - 1:
                    print("Maze solved: True")
                    return True
                
                # For backtracking visualization, we'll add cells in reverse order
                # so that we explore in a more logical order
                moves = []
                
                # Check up
                if (j > 0 and 
                    not current_cell.has_top_wall and 
                    not self.cells[i][j - 1].visited):
                    moves.append((i, j - 1))
                    
                # Check down
                if (j < self._num_rows - 1 and 
                    not current_cell.has_bottom_wall and 
                    not self.cells[i][j + 1].visited):
                    moves.append((i, j + 1))
                    
                # Check left
                if (i > 0 and 
                    not current_cell.has_left_wall and 
                    not self.cells[i - 1][j].visited):
                    moves.append((i - 1, j))
                    
                # Check right
                if (i < self._num_cols - 1 and 
                    not current_cell.has_right_wall and 
                    not self.cells[i + 1][j].visited):
                    moves.append((i + 1, j))
                
                # If we hit a dead end (no moves available)
                if not moves:
                    # Backtrack by undoing the last move
                    while path and not moves:
                        prev_cell, curr_cell = path.pop()
                        prev_cell.draw_move(curr_cell, undo=True)  # Draw gray line
                        
                        # Try to find a new move from the previous cell
                        prev_i = (prev_cell._x1 + prev_cell._x2) // (2 * self._cell_size_x)
                        prev_j = (prev_cell._y1 + prev_cell._y2) // (2 * self._cell_size_y)
                        
                        # Check for available moves from this previous position
                        if prev_i > 0 and not prev_cell.has_left_wall and not self.cells[prev_i - 1][prev_j].visited:
                            moves.append((prev_i - 1, prev_j))
                        if prev_i < self._num_cols - 1 and not prev_cell.has_right_wall and not self.cells[prev_i + 1][prev_j].visited:
                            moves.append((prev_i + 1, prev_j))
                        if prev_j > 0 and not prev_cell.has_top_wall and not self.cells[prev_i][prev_j - 1].visited:
                            moves.append((prev_i, prev_j - 1))
                        if prev_j < self._num_rows - 1 and not prev_cell.has_bottom_wall and not self.cells[prev_i][prev_j + 1].visited:
                            moves.append((prev_i, prev_j + 1))
                        
                        if moves:
                            stack.append((prev_i, prev_j, None))  # Add the backtrack position
                
                # Add all valid moves to the stack
                for next_i, next_j in moves:
                    stack.append((next_i, next_j, current_cell))
                    
            self._animate()
    
        print("Maze solved: False")
        return False
    