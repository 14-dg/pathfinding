# grid.py
from typing import Any, List
from cell import Cell
from constants import *

class Grid:
    def __init__(self, width: int, height: int, grid_name: str = MAIN_GRID) -> None:
        self.grid = []
        self.grid_name = grid_name
        
        self.targets = set()
        self.obstacles = set()
        self.starting_points = set()
        
        self.seen_points = set()
        self.current_path_points = set()
        self.way_points = set()
         
        self.width = width
        self.height = height
        self.create_grid()
        
    def create_grid(self) -> None:
        self.grid = [[] for h in range(self.height)]
        for row in range(0, self.height):
            for column in range(0, self.width):
                self.grid[row].append(Cell(row, column, grid_name=self.grid_name))
                
    def save_grid(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for row in self.grid:
                row_str = ','.join([cell.cell_type for cell in row])
                f.write(row_str + '\n')
                
    def load_grid(self, filename: str) -> None:
        with open(filename, 'r') as f:
            lines = f.readlines()
            self.height = len(lines)
            self.width = len(lines[0].strip().split(','))
            self.create_grid()
            for row_index, line in enumerate(lines):
                cell_types = line.strip().split(',')
                for col_index, cell_type in enumerate(cell_types):
                    self.find_and_change_type_of_cell((row_index, col_index), cell_type)
    
    def is_cell_unoccupied(self, cell_ind: tuple) -> bool:
        cell_row, cell_column = cell_ind
        cell = self.grid[cell_row][cell_column]
        return cell.cell_type not in [TARGET, STARTING_POINT, OBSTACLE]
    
    def change_type_of_cell(self, cell_ind: tuple, new_type: str) -> Cell | None:
        cell_row, cell_column = cell_ind
        self.grid[cell_row][cell_column].set_cell_type(new_type)
        return self.grid[cell_row][cell_column]
    
    def change_type_of_cell_target(self, cell_ind: tuple) -> List[Cell] | None:
        old_target = None
        if self.targets:
            old_target = self.targets.pop()
            if old_target:
                self.change_type_of_cell(old_target.get_cell_ind(), EMPTY)
            else:
                raise Exception("Error: old target cell not found in grid.")
        self.targets.add(self.change_type_of_cell(cell_ind, TARGET))
        if old_target:
            return [old_target, *self.targets]
        else:
            return [*self.targets]
        
    def change_type_of_cell_starting_point(self, cell_ind: tuple) -> List[Cell] | None:
        old_starting_point = None
        if self.starting_points:
            old_starting_point = self.starting_points.pop()
            if old_starting_point:
                self.change_type_of_cell(old_starting_point.get_cell_ind(), EMPTY)
            else:
                raise Exception("Error: old starting point cell not found in grid.")
        self.starting_points.add(self.change_type_of_cell(cell_ind, STARTING_POINT))
        if old_starting_point:
            return [old_starting_point, *self.starting_points]
        else:
            return [*self.starting_points]
        
    def change_type_of_cell_seen_point(self, cell_ind: tuple) -> Cell | None:
        if self.is_cell_unoccupied(cell_ind):
            cell = self.grid[cell_ind[0]][cell_ind[1]]
            self.seen_points.add(cell)
            return self.change_type_of_cell(cell_ind, SEEN_POINT)
        
    def change_type_of_cell_current_path_points(self, cell_ind: tuple) -> Cell | None:
        if self.is_cell_unoccupied(cell_ind):
            cell = self.grid[cell_ind[0]][cell_ind[1]]
            self.current_path_points.add(cell)
            return self.change_type_of_cell(cell_ind, CURRENT_PATH_CELL)
    
    def change_type_of_cell_way_point(self, cell_ind: tuple) -> Cell | None:
        if self.is_cell_unoccupied(cell_ind):
            cell = self.grid[cell_ind[0]][cell_ind[1]]
            if cell.cell_type == CURRENT_PATH_CELL:
                self.current_path_points.discard(cell)
            self.way_points.add(cell)
            return self.change_type_of_cell(cell_ind, WAY_POINT)
        
    def change_type_of_cell_obstacle(self, cell_ind: tuple) -> Cell | None:
        cell = self.grid[cell_ind[0]][cell_ind[1]]
        if cell.cell_type != OBSTACLE:
            self.obstacles.add(cell)
            return self.change_type_of_cell(cell_ind, OBSTACLE)
    
    def change_type_of_cell_empty(self, cell_ind: tuple) -> Cell | None:
        cell = self.grid[cell_ind[0]][cell_ind[1]]
        if cell.cell_type == OBSTACLE:
            self.obstacles.discard(cell)
        if cell.cell_type == TARGET:
            self.targets.discard(cell)
        if cell.cell_type == STARTING_POINT:
            self.starting_points.discard(cell)
        if cell.cell_type == SEEN_POINT:
            self.seen_points.discard(cell)
        if cell.cell_type == CURRENT_PATH_CELL:
            self.current_path_points.discard(cell)
        if cell.cell_type == WAY_POINT:
            self.way_points.discard(cell)
        return self.change_type_of_cell(cell_ind, EMPTY)
  
    def find_and_change_type_of_cell(self, cell_ind: tuple, new_type: str) -> List[Cell] | None:
        c = None
        if cell_ind:
            if new_type == TARGET:
                self.change_type_of_cell_empty(cell_ind)
                return self.change_type_of_cell_target(cell_ind)
            elif new_type == STARTING_POINT:
                self.change_type_of_cell_empty(cell_ind)
                return self.change_type_of_cell_starting_point(cell_ind)
            elif new_type == SEEN_POINT:
                c = self.change_type_of_cell_seen_point(cell_ind)
            elif new_type == CURRENT_PATH_CELL:
                c = self.change_type_of_cell_current_path_points(cell_ind)
            elif new_type == WAY_POINT:
                c = self.change_type_of_cell_way_point(cell_ind)
            elif new_type == OBSTACLE:
                self.change_type_of_cell_empty(cell_ind)
                c = self.change_type_of_cell_obstacle(cell_ind)
            elif new_type == EXPECTED_OCCUPIED:
                c = self.change_type_of_cell_empty(cell_ind)
                c = self.change_type_of_cell(cell_ind, EXPECTED_OCCUPIED)
            elif new_type == EXPECTED_FREE:
                c = self.change_type_of_cell_empty(cell_ind)
                c = self.change_type_of_cell(cell_ind, EXPECTED_FREE)
            elif new_type == ROVER_POSITION:
                c = self.change_type_of_cell_empty(cell_ind)
                c = self.change_type_of_cell(cell_ind, ROVER_POSITION)
            elif new_type == EMPTY:
                c = self.change_type_of_cell_empty(cell_ind)
            else:
                raise ValueError(f"Unknown cell type: {new_type}")
        if c:
            return [c]
        return None
    
    def clear_current_path_points(self) -> list[Cell]:
        temp = list(self.current_path_points)
        for cell in temp:   # über die Kopie iterieren, nicht über das Original
            self.change_type_of_cell_empty(cell.get_cell_ind())
        self.current_path_points = set()
        return temp
    
    def clear_board(self) -> None:
        for row in self.grid:
            for c in row:
                if c:
                    self.change_type_of_cell_empty(c.get_cell_ind())
        self.targets = set()
        self.obstacles = set()
        self.starting_points = set()
        self.seen_points = set()
        self.current_path_points = set()
        self.way_points = set()
        
    def clear_board_of_pathfinding_types(self) -> List[Cell]:
        removed_cells = []
        for x in self.grid:
            for c in x:
                if c.cell_type in [SEEN_POINT, CURRENT_PATH_CELL, WAY_POINT]:
                    if c not in self.starting_points:
                        removed_cells.append(c)
                        self.change_type_of_cell_empty(c.get_cell_ind())
        self.seen_points = set()
        self.current_path_points = set()
        self.way_points = set()
        return removed_cells
        
    def get_adjacent_cells(self, cell: Cell) -> List[Cell] | None:
        adjacent_cells = []
        if cell:
            row, column = cell.get_cell_ind()
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for direction in directions:
                new_column = column + direction[0]
                new_row = row + direction[1]
                if 0 <= new_column < self.width and 0 <= new_row < self.height:
                    adjacent_cells.append(self.grid[new_row][new_column])
        if adjacent_cells == []:
            return None
        return adjacent_cells
    
    def get_adjacent_non_obstacle_cells(self, cell: Cell) -> List[Cell] | None:
        adjacent_cells = self.get_adjacent_cells(cell)
        if not adjacent_cells:
            return None
        adjacent_cells_empty = []
        for cell in adjacent_cells:
            if cell.cell_type != OBSTACLE:
                adjacent_cells_empty.append(cell)
        if adjacent_cells_empty == []:
            return None
        return adjacent_cells_empty
                
    def get_cells_of_type(self, cell_type: str) -> list:
        cells = []
        for h in self.grid:
            for c in h:
                if c.cell_type == cell_type:
                    cells.append(c)
        return cells