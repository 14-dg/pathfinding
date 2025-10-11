
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder
from drawing_board import DrawingBoard




def main():
    g = Grid()
    pf = Pathfinder(g)
    db = DrawingBoard(g, pf)
    db.mainloop()

if __name__ == "__main__":
    main()