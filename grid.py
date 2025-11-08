from typing import Any, List
from random import randint
from cell import Cell
from constants import *

class Grid:
    def __init__(self, width: int, height: int, grid_name: str = MAIN_GRID) -> None:
        self.grid = []
        self.grid_name = grid_name
        
        self.targets = []
        self.obstacles = []
        self.starting_points = []
        
        self.seen_points = []
        self.way_points = []
         
        self.width = width
        self.height = height
        self.create_grid()
        
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        
    def create_grid(self) -> None:
        self.grid = [[] for h in range(self.height)]
        
        for row in range(0, self.height):
            for column in range(0, self.width):
                self.grid[row].append(Cell(row, column, grid_name=self.grid_name))
    
    def is_cell_unoccupied(self, cell_ind: tuple) -> bool:
        cell_row, cell_column  = cell_ind[0], cell_ind[1]
        cell = self.grid[cell_row][cell_column]
        if cell.cell_type in [TARGET, STARTING_POINT, OBSTACLE]:
            return False
        return True
    
    def change_type_of_cell(self, cell_ind: tuple, new_type: str) -> Cell|None:
        cell_row, cell_column  = cell_ind[0], cell_ind[1]
        self.grid[cell_row][cell_column].set_cell_type(new_type)
        return self.grid[cell_row][cell_column]
    
    def change_type_of_cell_target(self, cell_ind: tuple) -> List[Cell]|None:
        old_target = None
        if self.targets:
            old_target = self.targets.pop()
            if old_target:             
                self.change_type_of_cell(old_target.get_cell_ind(), EMPTY)
            else:
                raise Exception("Error: old target cell not found in grid.")    
        
        self.targets.append(self.change_type_of_cell(cell_ind, TARGET))
        
        if old_target:
            return [old_target, *self.targets]
        else:
            return [*self.targets]
        
    def change_type_of_cell_starting_point(self, cell_ind: tuple) -> List[Cell]|None:
        old_starting_point = None
        if self.starting_points:
            old_starting_point = self.starting_points.pop()
            if old_starting_point:            
                self.change_type_of_cell(old_starting_point.get_cell_ind(), EMPTY)
            else:
                raise Exception("Error: old starting point cell not found in grid.")    
        
        self.starting_points.append(self.change_type_of_cell(cell_ind, STARTING_POINT))
        
        if old_starting_point:
            return [old_starting_point, *self.starting_points]
        else:
            return [*self.starting_points]
        
    def change_type_of_cell_seen_point(self, cell_ind: tuple) -> Cell|None:
        if self.is_cell_unoccupied(cell_ind):
            self.seen_points.append(self.grid[cell_ind[0]][cell_ind[1]])
            return self.change_type_of_cell(cell_ind, SEEN_POINT)
    
    def change_type_of_cell_way_point(self, cell_ind: tuple) -> Cell|None:
        if self.is_cell_unoccupied(cell_ind):
            self.way_points.append(self.grid[cell_ind[0]][cell_ind[1]])
            return self.change_type_of_cell(cell_ind, WAY_POINT)
        
    def change_type_of_cell_obstacle(self, cell_ind: tuple) -> Cell|None:
        if self.grid[cell_ind[0]][cell_ind[1]] not in self.obstacles:
            self.obstacles.append(self.grid[cell_ind[0]][cell_ind[1]])
            return self.change_type_of_cell(cell_ind, OBSTACLE)
    
    def change_type_of_cell_empty(self, cell_ind: tuple) -> Cell|None:
        cell = self.grid[cell_ind[0]][cell_ind[1]]
        if cell in self.obstacles:
            self.obstacles.remove(cell)
        if cell in self.targets:
            self.targets.remove(cell)
        if cell in self.starting_points:
            self.starting_points.remove(cell)
        if cell in self.seen_points:
            self.seen_points.remove(cell)
        if cell in self.way_points:
            self.way_points.remove(cell)
        return self.change_type_of_cell(cell_ind, EMPTY)
  
    def find_and_change_type_of_cell(self, cell_ind: tuple, new_type: str) -> List[Cell]|None:

        c = None
        if cell_ind:
            
            if new_type == TARGET:
                self.change_type_of_cell_empty(cell_ind)  # Reset cell to EMPTY before changing type
                return self.change_type_of_cell_target(cell_ind)
            
            elif new_type == STARTING_POINT:
                self.change_type_of_cell_empty(cell_ind)  # Reset cell to EMPTY before changing type
                return self.change_type_of_cell_starting_point(cell_ind)
            
            elif new_type == SEEN_POINT:
                c = self.change_type_of_cell_seen_point(cell_ind)
                
            elif new_type == WAY_POINT:
                c = self.change_type_of_cell_way_point(cell_ind)
                
            elif new_type == OBSTACLE:
                self.change_type_of_cell_empty(cell_ind)  # Reset cell to EMPTY before changing type
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
    
    def clear_board(self) -> None:
        for ind_y, row in enumerate(self.grid):
            for ind_x, c in enumerate(row):
                if c:
                    self.change_type_of_cell_empty(c.get_cell_ind())
                    
        self.targets = []
        self.obstacles = []
        self.starting_points = []
        
        self.seen_points = []
        self.way_points = []
                    
    def get_adjacent_cells(self, cell: Cell) -> List[Cell]|None:
        adjacent_cells = []
        if cell:
            row, column  = cell.get_cell_ind()
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),     # left, right, up, down
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]   # up-left, down-left, up-right, down-right
            for direction in directions:
                new_column = column + direction[0]
                new_row = row + direction[1]
                if 0 <= new_column < self.width and 0 <= new_row < self.height:
                    adjacent_cells.append(self.grid[new_row][new_column])
                else:
                    pass
                    # adjacent_cells.append(None)
        if adjacent_cells == []:
            return None
        return adjacent_cells
    
    def get_adjacent_non_obstacle_cells(self, cell: Cell) -> List[Cell]|None:
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
    

    
    
if __name__ == "__main__":
    g = Grid(10, 10)
    print("Initial Grid:")
    for row in g.grid:
        print(row)
    
    print("\nChanging cell (2,3) to OBSTACLE:")
    g.change_type_of_cell_obstacle((2, 3))
    for row in g.grid:
        print(row)
    
    print("\nChanging cell (5,5) to TARGET:")
    g.change_type_of_cell_target((5, 5))
    for row in g.grid:
        print(row)
    
    print("\nAdjacent cells to (5,5):")
    target_cell = g.grid[5][5]
    adjacent_cells = g.get_adjacent_cells(target_cell)
    print(adjacent_cells)