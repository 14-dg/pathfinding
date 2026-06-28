# sensor_data.py
import math
from random import randint

from constants import *
from cell import Cell
from grid import Grid

def simulate_lidar_scan(grid: Grid, position: tuple, scan_range: int = 15, 
                        points_per_rotation: int = 360, noise_factor_per: int = 0
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
            noise = randint(0, int(noise_factor_per)) / 100.0
            scan_row = int(round(pos_row + r * math.sin(rad)))
            scan_col = int(round(pos_col + r * math.cos(rad)))
            
            if 0 <= scan_row < grid.height and 0 <= scan_col < grid.width:
                cell = grid.grid[scan_row][scan_col]
                
                if cell.cell_type == OBSTACLE:
                    noise_offset = int(round(noise * r))
                    scan_row_noise = scan_row + randint(-noise_offset, noise_offset)
                    scan_col_noise = scan_col + randint(-noise_offset, noise_offset)
                    scan_row_noise = max(0, min(grid.height - 1, scan_row_noise))
                    scan_col_noise = max(0, min(grid.width - 1, scan_col_noise))
                    occupied_cells.add((scan_row_noise, scan_col_noise))
                    break
                elif cell.cell_type in [SEEN_POINT, CURRENT_PATH_CELL, WAY_POINT]:
                    continue
                else:
                    free_cells.add((scan_row, scan_col))
            else:
                break
    
    return free_cells, occupied_cells