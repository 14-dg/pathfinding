
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder
from drawing_board import DrawingBoard




def main():
    g = Grid(70, 40, 20, 2)
    db = DrawingBoard(g)
    db.mainloop()

if __name__ == "__main__":
    main()