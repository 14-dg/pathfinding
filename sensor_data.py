
import math

from constants import *
from cell import Cell
from grid import Grid

        
import math

def simulate_lidar_scan(grid: Grid, position: tuple, scan_range: int = 10, 
                        points_per_rotation: int = 360
                        ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """
    Simulates a 360° LIDAR scan.
    Returns:
        free_cells: set of (row, col) tuples where the beam passed (no obstacle)
        occupied_cells: set of (row, col) tuples where an obstacle was detected
    """
    free_cells = set()
    occupied_cells = set()
    
    pos_row, pos_col = position
    angle_step = max(1, 360 // points_per_rotation)
    
    for angle in range(0, 360, angle_step):
        rad = math.radians(angle)
        
        for r in range(1, scan_range + 1):
            scan_row = int(round(pos_row + r * math.sin(rad)))
            scan_col = int(round(pos_col + r * math.cos(rad)))
            
            if 0 <= scan_row < grid.height and 0 <= scan_col < grid.width:
                cell = grid.grid[scan_row][scan_col]
                
                if cell.cell_type == OBSTACLE:
                    occupied_cells.add((scan_row, scan_col))
                    break  # hit obstacle → stop this ray
                elif cell.cell_type in [SEEN_POINT, CURRENT_PATH_CELL, WAY_POINT]:
                    continue  # ignore these special cells
                else:
                    free_cells.add((scan_row, scan_col))
            else:
                break  # out of bounds
    
    return free_cells, occupied_cells



if __name__ == "__main__":
    g = Grid(50, 50)
    g.grid[30][30].set_cell_type(OBSTACLE)
    g.grid[20][25].set_cell_type(OBSTACLE)
    g.grid[40][35].set_cell_type(OBSTACLE)
    g.grid[25][40].set_cell_type(OBSTACLE)
    g.grid[10][10].set_cell_type(OBSTACLE)
    g.grid[45][20].set_cell_type(OBSTACLE)
    g.grid[15][30].set_cell_type(OBSTACLE)    
    
    free_cells, occupied_cells = simulate_lidar_scan(g, (25, 25))
    print("Free cells detected by LIDAR: ", free_cells)
    print("Occupied cells detected by LIDAR: ", occupied_cells)