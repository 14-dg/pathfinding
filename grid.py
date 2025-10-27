from typing import Any, List
from random import randint
from cell import Cell
from constants import *

class Grid:
    def __init__(self, width: int, height: int, length_square: int, margin: int) -> None:
        self.grid_ind = []
        self.grid = []
        
        self.targets = []
        self.obstacles = []
        self.starting_points = []
        
        self.seen_points = []
        self.way_points = []
         
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
    
    def is_cell_unoccupied(self, cell_ind: tuple) -> bool:
        cell_x, cell_y = cell_ind[0], cell_ind[1]
        cell = self.grid[cell_y][cell_x]
        if cell.cell_type in [TARGET, STARTING_POINT, OBSTACLE]:
            return False
        return True
    
    def find_cell_hit(self, pos: tuple) -> tuple|None:
        pos_x, pos_y = pos[0], pos[1]
        cell_ind_x = pos_x // (self.length_squares + self.margin)
        cell_ind_y = pos_y // (self.length_squares + self.margin)
        
        if cell_ind_x < 0 or cell_ind_x >= self.width:
            cell_ind_x = -1
        if cell_ind_y < 0 or cell_ind_y >= self.height:
            cell_ind_y = -1
        
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
        
    def change_type_of_cell_seen_point(self, cell_ind: tuple) -> Cell|None:
        if self.is_cell_unoccupied(cell_ind):
            self.seen_points.append(self.grid[cell_ind[1]][cell_ind[0]])
            return self.change_type_of_cell(cell_ind, SEEN_POINT)
    
    def change_type_of_cell_way_point(self, cell_ind: tuple) -> Cell|None:
        if self.is_cell_unoccupied(cell_ind):
            self.way_points.append(self.grid[cell_ind[1]][cell_ind[0]])
            return self.change_type_of_cell(cell_ind, WAY_POINT)
        
    def change_type_of_cell_obstacle(self, cell_ind: tuple) -> Cell|None:
        if self.grid[cell_ind[1]][cell_ind[0]] not in self.obstacles:
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
        if cell in self.seen_points:
            self.seen_points.remove(cell)
        if cell in self.way_points:
            self.way_points.remove(cell)
        return self.change_type_of_cell(cell_ind, EMPTY)
  
    def find_and_change_type_of_cell(self, pos: tuple, new_type: str) -> List[Cell]|None:
        cell_ind = self.find_cell_hit(pos)

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
                
            elif new_type == EMPTY:
                c = self.change_type_of_cell_empty(cell_ind)
            else:
                raise ValueError(f"Unknown cell type: {new_type}")
        if c:
            return [c]
        return None
    
    def clear_board(self) -> None:
        for ind_y, h in enumerate(self.grid):
            for ind_x, c in enumerate(h):
                cell_ind = self.find_cell_hit((c.x, c.y))
                if cell_ind:
                    self.change_type_of_cell_empty(cell_ind)
                    
        self.targets = []
        self.obstacles = []
        self.starting_points = []
        
        self.seen_points = []
        self.way_points = []
                    
    def get_adjacent_cells(self, cell: Cell) -> List[Cell]|None:
        adjacent_cells = []
        cell_ind = self.find_cell_hit((cell.x, cell.y))
        if cell_ind:
            x, y = cell_ind[0], cell_ind[1]
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1),     # left, right, up, down
                          (-1, -1), (-1, 1), (1, -1), (1, 1)]   # up-left, down-left, up-right, down-right
            for direction in directions:
                new_x = x + direction[0]
                new_y = y + direction[1]
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    adjacent_cells.append(self.grid[new_y][new_x])
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
    
    def create_random_maze(self):
        for row in self.grid:
            for cell in row:
                n = randint(1, 100)

                pos = (cell.x, cell.y)
                if n<75:
                    self.find_and_change_type_of_cell(pos, EMPTY)
                elif n<=100:
                    self.find_and_change_type_of_cell(pos, OBSTACLE)
                                        
        target_cell = self.grid[int(0.1 * self.height)][int(0.1 * self.height)]
        pos_target = (target_cell.x, target_cell.y)
        starting_point_cell = self.grid[int(0.9 * self.height)][int(0.9 * self.width)]
        pos_starting_point = (starting_point_cell.x, starting_point_cell.y)
        self.find_and_change_type_of_cell(pos_target, TARGET)
        self.find_and_change_type_of_cell(pos_starting_point, STARTING_POINT)
    
if __name__ == "__main__":
    g = Grid(5, 5, 20, 2)
    print(g.grid_ind)
    for x in g.grid:
        print(x)
        
    print(g.get_screen_dimensions())
    
    print(g.find_cell_hit((2, 53)))
    print(g.find_cell_hit((23, 0)))
    print(g.find_cell_hit((43, 3)))