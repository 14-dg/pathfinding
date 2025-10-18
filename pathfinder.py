
from cell import Cell
from grid import Grid
from constants import *



class Pathfinder:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid

    def find(self):
        if self.grid.seen_points == []:
            self.grid.seen_points = self.grid.starting_points.copy()
        
        changed_cells = []
        
        sps = self.grid.seen_points.copy()
        for sp_c in sps:
            adjacent_cells = self.grid.get_adjacent_cells(sp_c)
            for a_c in adjacent_cells:
                if a_c:
                    cells = self.grid.find_and_change_type_of_cell((a_c.x, a_c.y), SEEN_POINT)
                    if cells:
                        changed_cells.extend(cells)
        return changed_cells


