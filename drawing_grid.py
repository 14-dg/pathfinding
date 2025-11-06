
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
        
        cell_column = int(round(pos_in_cell_x))
        cell_row = int(round(pos_in_cell_y))
        
        if 0 > cell_column or cell_column >= self.grid.width:
            cell_column = -1
        if 0 > cell_row or cell_row >= self.grid.height:
            cell_row = -1
        return (cell_row, cell_column)
    
    def get_pos_of_cell(self, cell_ind: tuple) -> tuple|None:
        cell_row, cell_column = cell_ind[0], cell_ind[1]
        if 0 > cell_column or cell_column >= self.grid.width:
            return None
        if 0 > cell_row or cell_row >= self.grid.height:
            return None
        
        x = self.offset_x + cell_column * (self.length_squares + self.margin)
        y = self.offset_y + cell_row * (self.length_squares + self.margin)
        return (x, y)
    
    def draw_cell(self, screen, c: Cell, x, y, w, h) -> None:
        pygame.draw.rect(screen , c.color, (x, y, w, h))
    
    def draw_board(self, screen):
        for row in self.draw_grid:
            for column in row:
                self.draw_cell(screen, *column)
                
    def clear_board(self, screen):
        self.grid.clear_board()
        self.draw_board(screen)
        
    def find_and_change_type_of_cell(self, screen, pos: tuple, cell_type: str) -> None:
        cell_ind = self.find_cell_hit(pos)
        if cell_ind:
            cell_list = self.grid.find_and_change_type_of_cell(cell_ind, cell_type)
            if cell_list:
                for cell in cell_list:
                    pos_cell = self.get_pos_of_cell(cell_ind)
                    if pos_cell:
                        self.draw_cell(screen, cell, pos_cell[0], pos_cell[1], self.length_squares, self.length_squares)
        return None
                
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