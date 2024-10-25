from maze import Window, Line, Point, Cell, Maze


def main():
    window = Window(800, 600)

    num_cols = 12
    num_rows = 10
    Maze(0, 0, num_rows, num_cols, 10, 10, window)

    window.wait_for_close()



if __name__ == "__main__":
    main()
