
from constants import *
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder
from drawing_grid import DrawingGrid
from drawing_board import DrawingBoard




def main():
    g1 = Grid(80, 80, grid_name=MAIN_GRID)
    g2 = Grid(80, 80, grid_name=ROVER_GRID)
    g3 = Grid(80, 80, grid_name=SENSOR_GRID)
    g4 = Grid(80, 80, grid_name=ROVER_PATHFINDER_GRID)
        
    dg1 = DrawingGrid(g1, 5, 1, 0, 0)
    dg2 = DrawingGrid(g2, 5, 1, dg1.get_screen_dimensions()[0]+10, 0)
    dg3 = DrawingGrid(g3, 5, 1, 0, dg1.get_screen_dimensions()[1]+10)
    dg4 = DrawingGrid(g4, 5, 1, dg3.get_screen_dimensions()[0]+10, dg1.get_screen_dimensions()[1]+10)
    
    db = DrawingBoard(MAIN_GRID=dg1, ROVER_GRID=dg2, SENSOR_GRID=dg3, ROVER_PATHFINDER_GRID=dg4)
    db.mainloop()

if __name__ == "__main__":
    print("controls: ")
    print("'left click':    (can also hold down): set obstacle")
    print("'right click':   set starting point")
    print("'middle click':  remove cell to empty")
    print("'p' key:         set target point")
    print("'c' key:         clear board where mouse is")
    print("'m' key:         create random maze where mouse is")
    print("'space' key:     remove all grids to empty")
    print("'enter' key:     run pathfinder")
    print("'j' key:         stop pathfinder and current path")
    print("'s' key:         show LIDAR scan from rover position")
    print("'r' key:         reset pathfinder and clear pathfinding types")
    print("'i' key:         show debug info")
    print("Note: Pathfinder runs on ROVER_PATHFINDER_GRID but shows data from MAIN_GRID and ROVER_GRID")
    main()