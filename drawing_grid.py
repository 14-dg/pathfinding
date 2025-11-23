
from typing import Any
from random import randint
import pygame

from cell import Cell
from grid import Grid
from constants import *

from sensor_data import simulate_lidar_scan


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
    
    def find_cell_hit(self, pos: tuple) -> tuple:
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
    
    def draw_cell(self, screen, c: Cell, x, y, w, h) -> None:
        pygame.draw.rect(screen , c.color, (x, y, w, h))
    
    def update_cell_on_screen(self, screen, cell: Cell) -> None:
        cell_ind = cell.get_cell_ind()
        if cell_ind:
            self.draw_cell(screen, *self.draw_grid[cell_ind[0]][cell_ind[1]])
        else:
            print("Could not get position of cell:", cell)
    
    def draw_board(self, screen):
        for row in self.draw_grid:
            for column in row:
                self.draw_cell(screen, *column)
                
    def clear_board(self):
        self.grid.clear_board()
        
    def clear_current_path(self, screen):
        removed_cells = self.grid.clear_current_path_points()
        for r_c in removed_cells:
            self.change_type_of_cell(screen, r_c.get_cell_ind(), SEEN_POINT)
        
    def change_type_of_cell(self, screen, cell_ind: tuple, cell_type: str) -> tuple[int, int]:
        cell_list = self.grid.find_and_change_type_of_cell(cell_ind, cell_type)
        if cell_list:
            for cell in cell_list:
                self.draw_cell(screen, *self.draw_grid[cell.row_ind][cell.column_ind])
        return cell_ind
        
    def find_and_change_type_of_cell(self, screen, pos: tuple, cell_type: str) -> tuple[int, int]:
        cell_ind = self.find_cell_hit(pos)
        if cell_ind:
            return self.change_type_of_cell(screen, cell_ind, cell_type)
        return cell_ind
                
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
        
    def show_sensor_data(self, screen, grid, start_cell: Cell) -> None:
        free_cells, occupied_cells = simulate_lidar_scan(grid, start_cell.get_cell_ind(), 
                                                            scan_range=20, points_per_rotation=180)
        # print("LIDAR Scan from", start_cell.get_cell_ind())
        # print("Free cells detected by LIDAR: ", free_cells)
        # print("Occupied cells detected by LIDAR: ", occupied_cells)
        
        for free_cell in free_cells:
            self.change_type_of_cell(screen, free_cell, EXPECTED_FREE)
        for occupied_cell in occupied_cells:
            self.change_type_of_cell(screen, occupied_cell, EXPECTED_OCCUPIED)
        self.change_type_of_cell(screen, start_cell.get_cell_ind(), ROVER_POSITION)
        
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