
from constants import *
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder
from drawing_grid import DrawingGrid
from drawing_board import DrawingBoard




def main():
    g1 = Grid(20, 20, grid_name=MAIN_GRID)
    g2 = Grid(20, 20, grid_name=SECONDARY_GRID)
    g3 = Grid(20, 20, grid_name=SECONDARY_GRID)
    g4 = Grid(20, 20, grid_name=SECONDARY_GRID)
        
    dg1 = DrawingGrid(g1, 20, 2, 0, 0)
    dg2 = DrawingGrid(g2, 20, 2, dg1.get_screen_dimensions()[0]+10, 0)
    dg3 = DrawingGrid(g3, 20, 2, 0, dg1.get_screen_dimensions()[1]+10)
    dg4 = DrawingGrid(g4, 20, 2, dg3.get_screen_dimensions()[0]+10, dg1.get_screen_dimensions()[1]+10)
    
    db = DrawingBoard(MAIN_GRID=dg1, SECONDARY_GRID=dg2, THIRD_GRID=dg3)#, FOURTH_GRID=dg4)
    db.mainloop()

if __name__ == "__main__":
    main()