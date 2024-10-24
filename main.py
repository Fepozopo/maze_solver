from window import Window, Point, Line


def main():
    window = Window(800, 600)

    # Draw a few lines
    window.draw_line(Line(Point(0, 0), Point(800, 600)), 'black')
    window.draw_line(Line(Point(0, 600), Point(800, 0)), 'black')

    window.wait_for_close()




if __name__ == "__main__":
    main()
