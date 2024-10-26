import unittest
from maze import Maze



class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )

    def test_maze_draw_cell(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._draw_cell(0, 0)
        self.assertEqual(
            m1.cells[0][0]._x1,
            0,
        )
        self.assertEqual(
            m1.cells[0][0]._y1,
            0,
        )
        self.assertEqual(
            m1.cells[0][0]._x2,
            10,
        )
        self.assertEqual(
            m1.cells[0][0]._y2,
            10,
        )
        self.assertEqual(
            m1.cells[0][0]._win,
            m1._win,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        self.assertEqual(
            m1.entrance_cell.has_top_wall,
            False,
        )
        self.assertEqual(
            m1.exit_cell.has_bottom_wall,
            False,
        )



if __name__ == "__main__":
    unittest.main()