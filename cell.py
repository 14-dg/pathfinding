from __future__ import annotations

from constants import *

class Cell:
    def __init__(self, x: int, y: int, w: int, h: int, 
                 cell_type: str = EMPTY) -> None:
        self.x = x
        self.y = y
        self.w = w
        self.h = h        
  
        self.set_cell_type(cell_type)
        
    def __repr__(self) -> str:
        return f"Cell({self.x}, {self.y}, {self.w}, {self.h}, {self.cell_type})"
    
    def __hash__(self) -> int:
        "leaves out type so it does not afffect hashing"
        return hash((self.x, self.y, self.w, self.h))
    
    def __eq__(self, value: object) -> bool:
        "leaves out type so it does not afffect equality"
        return isinstance(value, Cell) and (self.x, self.y, self.w, self.h) == (value.x, value.y, value.w, value.h)
        
    def set_cell_type(self, cell_type: str) -> None:
        self.cell_type = cell_type
        self.color = cell_color[cell_type]
        
    def inside_cell(self, pos: tuple) -> bool:
        if self.x <= pos[0] <= self.x + self.w and self.y <= pos[1] <= self.y + self.h:
            return True
        return False
    
    def dist(self, other: Cell) -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
        
if __name__ == "__main__":
    c = Cell(0, 0, 20, 20, cell_type=TARGET)
    print(c.x, c.y, c.w, c.h, c.cell_type, c.color)