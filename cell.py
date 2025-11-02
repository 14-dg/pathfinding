from __future__ import annotations

from constants import *

class Cell:
    def __init__(self, row_ind: int, column_ind: int, cell_type: str = EMPTY, grid_name: str = MAIN_GRID) -> None:
        self.row_ind = row_ind
        self.column_ind = column_ind
        
        self.grid_name = grid_name
        
        # they get set in set_cell_type
        self.cell_type = None
        self.color = None  
        self.set_cell_type(cell_type)
        
    def __repr__(self) -> str:
        return f"Cell({self.row_ind}, {self.column_ind}, {self.cell_type}, {self.grid_name})"
    
    def __hash__(self) -> int:
        "leaves out type so it does not afffect hashing"
        return hash((self.row_ind, self.column_ind, self.grid_name))
    
    def __eq__(self, value: object) -> bool:
        "leaves out type so it does not afffect equality"
        return isinstance(value, Cell) and (self.grid_name, self.row_ind, self.column_ind) == (value.grid_name, value.row_ind, value.column_ind)        
    
    def get_cell_ind(self) -> tuple:
        '''returns (row_ind, column_ind)'''
        return (self.row_ind, self.column_ind)
    
    def set_cell_type(self, cell_type: str) -> None:
        self.cell_type = cell_type
        self.color = cell_color[cell_type]
    
    def dist(self, other: Cell) -> float:
        return ((self.row_ind - other.row_ind) ** 2 + (self.column_ind - other.column_ind) ** 2) ** 0.5
    
        
if __name__ == "__main__":
    c1 = Cell(2, 3, STARTING_POINT)
    c2 = Cell(2, 3, TARGET)
    c3 = Cell(4, 5, OBSTACLE)
    
    print(c1)
    print(c2)
    print(c3)
    
    print("c1 == c2:", c1 == c2)
    print("c1 == c3:", c1 == c3)
    
    cell_set = {c1, c2, c3}
    print("Cell set:", cell_set)