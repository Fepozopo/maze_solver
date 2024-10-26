from maze import Window, Line, Point, Cell, Maze


def main():
    window = Window(800, 600)
    num_cols = 16
    num_rows = 12
    
    maze = Maze(0, 0, num_rows, num_cols, 50, 50, window)

    window.wait_for_close()



if __name__ == "__main__":
    main()
