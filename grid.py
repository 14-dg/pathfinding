from typing import Any
from cell import Cell
from constants import *

class Grid:
    def __init__(self, width: int, height: int, length_square: int, margin: int) -> None:
        self.grid_ind = []
        self.grid = []
        
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
        
    def find_and_change_type_of_cell(self, pos: tuple, new_type: str) -> Cell|None:
        cell_ind = self.find_cell_hit(pos)
        if cell_ind:
            return self.change_type_of_cell(cell_ind, new_type)
        return None
    
    def clear_board(self) -> None:
        for h in self.grid:
            for c in h:
                c.set_cell_type(EMPTY)
    
if __name__ == "__main__":
    g = Grid(5, 5, 20, 2)
    print(g.grid_ind)
    for x in g.grid:
        print(x)
        
    print(g.get_screen_dimensions())
    
    print(g.find_cell_hit((2, 53)))
    print(g.find_cell_hit((23, 0)))
    print(g.find_cell_hit((43, 3)))