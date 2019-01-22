from classmaze import Maze
from classgraphics import Graphics


def main():
    laby = Maze("maze.txt")
    gui = Graphics(laby)
    gui.main_loop()


if __name__ == "__main__":
    main()
