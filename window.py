from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.width = width
        self.height = height
        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        '''
        Call the root widget's update_idletasks() and update() methods to redraw the canvas.
        '''
        self.root.update_idletasks()
        self.root.update()

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
