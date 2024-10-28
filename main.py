from maze import Window, Maze
from time import sleep


def main():
    win = Window(800, 600)
    num_cols = 15
    num_rows = 11
    
    print("Generating maze...")
    maze = Maze(10, 10, num_rows, num_cols, 50, 50, win)
    
    # Pause briefly to see the generated maze
    print("Maze generated. Starting solve in 1 second...")
    sleep(1)
    
    # Try to solve the maze
    solved = maze.solve()
    
    if solved:
        print("Solution found! Close the window to exit.")
    else:
        print("No solution found! Close the window to exit.")

    # Keep window open
    win.wait_for_close()



if __name__ == "__main__":
    main()
