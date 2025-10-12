from typing import Any
from cell import Cell

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
                self.grid[column].append((row * (self.length_squares + self.margin), 
                                          column * (self.length_squares + self.margin),
                                          self.length_squares, 
                                          self.length_squares))
                        
    def get_screen_dimensions(self) -> tuple:
        screen_width = self.width * (self.length_squares + self.margin) + self.margin
        screen_height = self.height * (self.length_squares + self.margin) + self.margin
        return (screen_width, screen_height)
    
if __name__ == "__main__":
    g = Grid(5, 5, 20, 2)
    print(g.grid_ind)
    for x in g.grid:
        print(x)