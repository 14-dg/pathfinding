
from constants import *
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder
from drawing_grid import DrawingGrid
from drawing_board import DrawingBoard




def main():
    g1 = Grid(35, 40, grid_name=MAIN_GRID)
    g2 = Grid(35, 40, grid_name=SECONDARY_GRID)
    
    dg1 = DrawingGrid(g1, 20, 2, 0, 0)
    dg2 = DrawingGrid(g2, 20, 2, dg1.get_screen_dimensions()[0], 0)
    
    db = DrawingBoard(dg1=dg1, dg2=dg2)
    db.mainloop()

if __name__ == "__main__":
    main()