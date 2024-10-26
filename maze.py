from tkinter import Tk, BOTH, Canvas
from time import sleep


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
        '''
        Call the root widget's update_idletasks() and update() methods to redraw the canvas.
        '''
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        '''
        Set the data member we created to track the "running" state of the window to True.
        Next, it should call self.redraw() over and over as long as the running state remains True.
        '''
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
        
        # By default, all walls exist
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        
    def draw(self):
        """
        Draw the cell's walls based on their existence state
        """
        # Create lines for each existing wall
        if self.has_left_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))
            self._win.draw_line(line, "black")
            
        if self.has_top_wall:
            line = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
            self._win.draw_line(line, "black")
            
        if self.has_right_wall:
            line = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")
            
        if self.has_bottom_wall:
            line = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
            self._win.draw_line(line, "black")

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
        
        # Initialize the grid of cells
        self.cells = []
        self._create_cells()
        
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
            sleep(0.05)