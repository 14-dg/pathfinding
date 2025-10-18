from typing import Any, List
from cell import Cell
from constants import *

class Grid:
    def __init__(self, width: int, height: int, length_square: int, margin: int) -> None:
        self.grid_ind = []
        self.grid = []
        
        self.targets = []
        self.obstacles = []
        self.starting_points = []
         
        self.width = width
        self.height = height
        self.length_squares = length_square
        self.margin = margin
        self.create_grid()
        
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        
    def create_grid(self) -> None:
        self.grid_ind = [[] for h in range(self.height)]
        self.grid = [[] for h in range(self.height)]
        
        for column in range(0, self.height):
            for row in range(0, self.width):
                self.grid_ind[column].append(row)
                self.grid[column].append(Cell(self.margin + row * (self.length_squares + self.margin), 
                                          self.margin + column * (self.length_squares + self.margin),
                                          self.length_squares, 
                                          self.length_squares))
                        
    def get_screen_dimensions(self) -> tuple:
        screen_width = self.width * (self.length_squares + self.margin) + self.margin
        screen_height = self.height * (self.length_squares + self.margin) + self.margin
        return (screen_width, screen_height)
    
    def find_cell_hit(self, pos: tuple) -> tuple|None:
        pos_x, pos_y = pos[0], pos[1]
        cell_ind_x = pos_x // (self.length_squares + self.margin)
        cell_ind_y = pos_y // (self.length_squares + self.margin)
        
        if self.grid[cell_ind_y][cell_ind_x].inside_cell(pos):
            return (cell_ind_x, cell_ind_y)
        return None
    
    def change_type_of_cell(self, cell_ind: tuple, new_type: str) -> Cell|None:
        cell_x, cell_y = cell_ind[0], cell_ind[1]
        self.grid[cell_y][cell_x].set_cell_type(new_type)
        return self.grid[cell_y][cell_x]
    
    def change_type_of_cell_target(self, cell_ind: tuple) -> List[Cell]|None:
        old_target = None
        if self.targets:
            old_target = self.targets.pop()
            old_target_cell_ind = self.find_cell_hit((old_target.x, old_target.y))
            if old_target_cell_ind:             
                self.change_type_of_cell(old_target_cell_ind, EMPTY)
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
            old_starting_point_cell_ind = self.find_cell_hit((old_starting_point.x, old_starting_point.y))
            if old_starting_point_cell_ind:            
                self.change_type_of_cell(old_starting_point_cell_ind, EMPTY)
            else:
                raise Exception("Error: old starting point cell not found in grid.")    
        
        self.starting_points.append(self.change_type_of_cell(cell_ind, STARTING_POINT))
        
        if old_starting_point:
            return [old_starting_point, *self.starting_points]
        else:
            return [*self.starting_points]
        
    def change_type_of_cell_obstacle(self, cell_ind: tuple) -> Cell|None:
        self.obstacles.append(self.grid[cell_ind[1]][cell_ind[0]])
        return self.change_type_of_cell(cell_ind, OBSTACLE)
    
    def change_type_of_cell_empty(self, cell_ind: tuple) -> Cell|None:
        cell = self.grid[cell_ind[1]][cell_ind[0]]
        if cell in self.obstacles:
            self.obstacles.remove(cell)
        if cell in self.targets:
            self.targets.remove(cell)
        if cell in self.starting_points:
            self.starting_points.remove(cell)
        return self.change_type_of_cell(cell_ind, EMPTY)
  
    def find_and_change_type_of_cell(self, pos: tuple, new_type: str) -> List[Cell]|None:
        cell_ind = self.find_cell_hit(pos)

        c = None
        if cell_ind:
            self.change_type_of_cell_empty(cell_ind)  # Reset cell to EMPTY before changing type
            
            if new_type == TARGET:
                return self.change_type_of_cell_target(cell_ind)
            elif new_type == STARTING_POINT:
                return self.change_type_of_cell_starting_point(cell_ind)
            elif new_type == OBSTACLE:
                c = self.change_type_of_cell_obstacle(cell_ind)
            else:
                c = self.change_type_of_cell(cell_ind, new_type)
        if c:
            return [c]
        return None
    
    def clear_board(self) -> None:
        for ind_y, h in enumerate(self.grid):
            for ind_x, c in enumerate(h):
                cell_ind = self.find_cell_hit((c.x, c.y))
                if cell_ind:
                    self.change_type_of_cell_empty(cell_ind)
                
    def get_cells_of_type(self, cell_type: str) -> list:
        cells = []
        for h in self.grid:
            for c in h:
                if c.cell_type == cell_type:
                    cells.append(c)
        return cells
    
if __name__ == "__main__":
    g = Grid(5, 5, 20, 2)
    print(g.grid_ind)
    for x in g.grid:
        print(x)
        
    print(g.get_screen_dimensions())
    
    print(g.find_cell_hit((2, 53)))
    print(g.find_cell_hit((23, 0)))
    print(g.find_cell_hit((43, 3)))