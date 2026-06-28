"""
Simulation eines 360° LIDAR-Sensors.
"""

from __future__ import annotations
import math
from random import randint
from typing import Tuple, Set

from constants import OBSTACLE, SEEN_POINT, CURRENT_PATH_CELL, WAY_POINT
from cell import Cell
from grid import Grid


class LidarSimulator:
    def __init__(
        self,
        scan_range: int = 15,
        points_per_rotation: int = 360,
        noise_percent: int = 0,
    ) -> None:
        self.scan_range = scan_range
        self.angle_step = max(1, 360 // points_per_rotation)
        self.noise_percent = noise_percent

    def simulate_scan(
        self, grid: Grid, position: tuple[int, int]
    ) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
        free = set()
        occupied = set()
        pos_row, pos_col = position

        for angle in range(0, 360, self.angle_step):
            rad = math.radians(angle)
            for r in range(1, self.scan_range + 1):
                noise = randint(0, self.noise_percent) / 100.0
                scan_row = int(round(pos_row + r * math.sin(rad)))
                scan_col = int(round(pos_col + r * math.cos(rad)))

                if not (0 <= scan_row < grid.height and 0 <= scan_col < grid.width):
                    break

                cell = grid.grid[scan_row][scan_col]

                if cell.cell_type == OBSTACLE:
                    noise_offset = int(round(noise * r))
                    nr = scan_row + randint(-noise_offset, noise_offset)
                    nc = scan_col + randint(-noise_offset, noise_offset)
                    nr = max(0, min(grid.height - 1, nr))
                    nc = max(0, min(grid.width - 1, nc))
                    occupied.add((nr, nc))
                    break
                elif cell.cell_type in (SEEN_POINT, CURRENT_PATH_CELL, WAY_POINT):
                    continue
                else:
                    free.add((scan_row, scan_col))
        return free, occupied


def simulate_lidar_scan(
    grid: Grid,
    position: tuple[int, int],
    scan_range: int = 15,
    points_per_rotation: int = 360,
    noise_factor_per: int = 0,
) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    sim = LidarSimulator(scan_range, points_per_rotation, noise_factor_per)
    return sim.simulate_scan(grid, position)


if __name__ == "__main__":
    g = Grid(50, 50)
    g.find_and_change_type_of_cell((30, 30), OBSTACLE)
    sim = LidarSimulator()
    free, occ = sim.simulate_scan(g, (25, 25))
    print(f"Free: {len(free)}, Occupied: {len(occ)}")