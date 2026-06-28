"""
Repräsentation einer einzelnen Gitterzelle.
"""

from __future__ import annotations
from constants import EMPTY, MAIN_GRID, CELL_COLOR


class Cell:
    def __init__(
        self,
        row_ind: int,
        column_ind: int,
        cell_type: str = EMPTY,
        grid_name: str = MAIN_GRID,
    ) -> None:
        self.row_ind = row_ind
        self.column_ind = column_ind
        self.grid_name = grid_name

        self.cell_type: str = cell_type
        self.color: tuple[int, int, int] = CELL_COLOR[cell_type]

    def __repr__(self) -> str:
        return f"Cell({self.row_ind}, {self.column_ind}, {self.cell_type}, {self.grid_name})"

    def __hash__(self) -> int:
        return hash((self.row_ind, self.column_ind, self.grid_name))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            return NotImplemented
        return (self.grid_name, self.row_ind, self.column_ind) == (
            other.grid_name,
            other.row_ind,
            other.column_ind,
        )

    def get_cell_ind(self) -> tuple[int, int]:
        return (self.row_ind, self.column_ind)

    def set_cell_type(self, cell_type: str) -> None:
        self.cell_type = cell_type
        self.color = CELL_COLOR[cell_type]

    def dist(self, other: Cell) -> float:
        return ((self.row_ind - other.row_ind) ** 2 + (self.column_ind - other.column_ind) ** 2) ** 0.5


if __name__ == "__main__":
    c1 = Cell(2, 3, TARGET := 'target')
    c2 = Cell(2, 3, 'obstacle')
    c3 = Cell(4, 5, 'obstacle')
    print(c1, c2, c3)
    assert c1 == c2
    assert c1 != c3
    print("Cell tests passed.")