
from typing import Any
from random import randint
import pygame

from cell import Cell
from grid import Grid
from constants import *


class DrawingGrid:
    def __init__(self, grid: Grid, length_square: int, margin: int, offset_x: int, offset_y: int) -> None:
        self.grid = grid        
        self.length_squares = length_square
        self.margin = margin
        
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.screen_width = (self.length_squares + self.margin) * self.grid.width - self.margin
        self.screen_height = (self.length_squares + self.margin) * self.grid.height - self.margin
        
        self.draw_grid: list[list[tuple[Cell, int, int, int, int]]] = []
        self.create_draw_grid()
        
    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
        
    def create_draw_grid(self) -> None:
        self.draw_grid = [[] for r in range(self.grid.height)]
        
        for row_ind, row in enumerate(self.grid.grid):
            for column_ind, cell in enumerate(row):
                x = self.offset_x + column_ind * (self.length_squares + self.margin)
                y = self.offset_y + row_ind * (self.length_squares + self.margin)
                w = self.length_squares
                h = self.length_squares
                self.draw_grid[row_ind].append((self.grid.grid[row_ind][column_ind], x, y, w, h))
        

    def get_screen_dimensions(self) -> tuple:
        width = self.screen_width
        height = self.screen_height
        width += self.offset_x
        height += self.offset_y
        return (width, height)
    
    def find_cell_hit(self, pos: tuple) -> tuple|None:
        pos_x, pos_y = pos[0], pos[1]
        pos_in_cell_x = (pos_x - self.offset_x) / (self.length_squares + self.margin)
        pos_in_cell_y = (pos_y - self.offset_y) / (self.length_squares + self.margin)
        
        cell_ind_x = int(round(pos_in_cell_x))
        cell_ind_y = int(round(pos_in_cell_y))
        
        if 0 <= cell_ind_x or cell_ind_x <= self.grid.width:
            cell_ind_x = -1
        if 0 <= cell_ind_y or cell_ind_y <= self.grid.height:
            cell_ind_y = -1
        return (cell_ind_x, cell_ind_y)
    
    def draw_cell(self, screen, c: Cell, x, y, w, h) -> None:
        pygame.draw.rect(screen , c.color, (x, y, w, h))
    
    def draw_board(self, screen):
        for row in self.draw_grid:
            for column in row:
                self.draw_cell(screen, *column)
                
    def create_random_maze(self):
        for row in self.grid.grid:
            for cell in row:
                n = randint(1, 100)
                if n<75:
                    self.grid.find_and_change_type_of_cell(cell.get_cell_ind(), EMPTY)
                elif n<=100:
                    self.grid.find_and_change_type_of_cell(cell.get_cell_ind(), OBSTACLE)
                                        
        target_cell = self.grid.grid[int(0.1 * self.grid.height)][int(0.1 * self.grid.height)]
        starting_point_cell = self.grid.grid[int(0.9 * self.grid.height)][int(0.9 * self.grid.width)]
        self.grid.find_and_change_type_of_cell(target_cell.get_cell_ind(), TARGET)
        self.grid.find_and_change_type_of_cell(starting_point_cell.get_cell_ind(), STARTING_POINT)
        
        
if __name__ == "__main__":
    g = Grid(10, 10)
    dg = DrawingGrid(g, 20, 2, 0, 0)
    print(dg.draw_grid)
    print("Screen dimensions:", dg.get_screen_dimensions())
    print("Cell hit at (15, 15):", dg.find_cell_hit((15, 15)))
    print("Cell hit at (50, 50):", dg.find_cell_hit((50, 50)))
    print("Cell hit at (250, 250):", dg.find_cell_hit((250, 250)))
    
    dg.create_random_maze()
    for row in dg.grid.grid:
        print(row)