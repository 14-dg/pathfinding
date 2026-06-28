"""
Datenmodell eines rechteckigen Gitters.
Bietet Operationen zum Setzen von Zelltypen und benachrichtigt Listener über Änderungen.
"""

from __future__ import annotations
import logging
from typing import Callable, List, Set, Tuple

from cell import Cell
from constants import *

logger = logging.getLogger(__name__)


class Grid:
    def __init__(self, width: int, height: int, grid_name: str = MAIN_GRID) -> None:
        self.width = width
        self.height = height
        self.grid_name = grid_name

        self.targets: set[Cell] = set()
        self.obstacles: set[Cell] = set()
        self.starting_points: set[Cell] = set()
        self.seen_points: set[Cell] = set()
        self.current_path_points: set[Cell] = set()
        self.way_points: set[Cell] = set()

        self._change_listeners: list[Callable[[Cell], None]] = []

        self.grid: list[list[Cell]] = []
        self._create_grid()

    # -------------------------------------------------------------------------
    #  Listener-System
    # -------------------------------------------------------------------------
    def add_change_listener(self, listener: Callable[[Cell], None]) -> None:
        self._change_listeners.append(listener)

    def _notify_change(self, cell: Cell) -> None:
        for listener in self._change_listeners:
            listener(cell)

    # -------------------------------------------------------------------------
    #  Gitter-Initialisierung
    # -------------------------------------------------------------------------
    def _create_grid(self) -> None:
        self.grid = [[Cell(row, col, grid_name=self.grid_name) for col in range(self.width)] for row in range(self.height)]

    # -------------------------------------------------------------------------
    #  Persistenz
    # -------------------------------------------------------------------------
    def save_grid(self, filename: str) -> None:
        with open(filename, 'w') as f:
            for row in self.grid:
                f.write(','.join(cell.cell_type for cell in row) + '\n')

    def load_grid(self, filename: str) -> None:
        with open(filename, 'r') as f:
            lines = f.readlines()
        self.height = len(lines)
        self.width = len(lines[0].strip().split(','))
        self._create_grid()
        for row_idx, line in enumerate(lines):
            for col_idx, cell_type in enumerate(line.strip().split(',')):
                self.find_and_change_type_of_cell((row_idx, col_idx), cell_type)

    # -------------------------------------------------------------------------
    #  Kern – Zelltyp ändern
    # -------------------------------------------------------------------------
    def change_type_of_cell(self, cell_ind: tuple[int, int], new_type: str) -> Cell:
        row, col = cell_ind
        cell = self.grid[row][col]
        cell.set_cell_type(new_type)
        self._notify_change(cell)
        return cell

    def is_cell_unoccupied(self, cell_ind: tuple[int, int]) -> bool:
        row, col = cell_ind
        return self.grid[row][col].cell_type not in (TARGET, STARTING_POINT, OBSTACLE)

    # -------------------------------------------------------------------------
    #  Interne Helfer – entfernen aus Spezialmengen ohne previous_type zu brauchen
    # -------------------------------------------------------------------------
    def _remove_from_sets(self, cell: Cell) -> None:
        """Entfernt eine Zelle aus allen Spezialmengen."""
        self.targets.discard(cell)
        self.obstacles.discard(cell)
        self.starting_points.discard(cell)
        self.seen_points.discard(cell)
        self.current_path_points.discard(cell)
        self.way_points.discard(cell)

    def _set_empty(self, cell_ind: tuple[int, int]) -> List[Cell]:
        cell = self.grid[cell_ind[0]][cell_ind[1]]
        self._remove_from_sets(cell)
        return [self.change_type_of_cell(cell_ind, EMPTY)]

    def _set_target(self, cell_ind: tuple[int, int]) -> List[Cell]:
        if self.targets:
            old = self.targets.pop()
            self._set_empty(old.get_cell_ind())
        cell = self.change_type_of_cell(cell_ind, TARGET)
        self.targets.add(cell)
        return [cell]

    def _set_starting_point(self, cell_ind: tuple[int, int]) -> List[Cell]:
        if self.starting_points:
            old = self.starting_points.pop()
            self._set_empty(old.get_cell_ind())
        cell = self.change_type_of_cell(cell_ind, STARTING_POINT)
        self.starting_points.add(cell)
        return [cell]

    def _set_obstacle(self, cell_ind: tuple[int, int]) -> List[Cell]:
        cell = self.grid[cell_ind[0]][cell_ind[1]]
        self._remove_from_sets(cell)                       # erst aus allen Mengen entfernen
        self.change_type_of_cell(cell_ind, OBSTACLE)       # Typ setzen
        self.obstacles.add(cell)
        return [cell]

    def _set_seen_point(self, cell_ind: tuple[int, int]) -> List[Cell] | None:
        if not self.is_cell_unoccupied(cell_ind):
            return None
        cell = self.change_type_of_cell(cell_ind, SEEN_POINT)
        self.seen_points.add(cell)
        return [cell]

    def _set_current_path_cell(self, cell_ind: tuple[int, int]) -> List[Cell] | None:
        if not self.is_cell_unoccupied(cell_ind):
            return None
        cell = self.change_type_of_cell(cell_ind, CURRENT_PATH_CELL)
        self.current_path_points.add(cell)
        return [cell]

    def _set_way_point(self, cell_ind: tuple[int, int]) -> List[Cell] | None:
        if not self.is_cell_unoccupied(cell_ind):
            return None
        cell = self.grid[cell_ind[0]][cell_ind[1]]
        if cell.cell_type == CURRENT_PATH_CELL:
            self.current_path_points.discard(cell)
        self.change_type_of_cell(cell_ind, WAY_POINT)
        self.way_points.add(cell)
        return [cell]

    def _set_expected_occupied(self, cell_ind: tuple[int, int]) -> List[Cell]:
        self._set_empty(cell_ind)
        return [self.change_type_of_cell(cell_ind, EXPECTED_OCCUPIED)]

    def _set_expected_free(self, cell_ind: tuple[int, int]) -> List[Cell]:
        self._set_empty(cell_ind)
        return [self.change_type_of_cell(cell_ind, EXPECTED_FREE)]

    def _set_rover_position(self, cell_ind: tuple[int, int]) -> List[Cell]:
        self._set_empty(cell_ind)
        return [self.change_type_of_cell(cell_ind, ROVER_POSITION)]

    _TYPE_HANDLERS = {
        TARGET: _set_target,
        STARTING_POINT: _set_starting_point,
        OBSTACLE: _set_obstacle,
        SEEN_POINT: _set_seen_point,
        CURRENT_PATH_CELL: _set_current_path_cell,
        WAY_POINT: _set_way_point,
        EXPECTED_OCCUPIED: _set_expected_occupied,
        EXPECTED_FREE: _set_expected_free,
        ROVER_POSITION: _set_rover_position,
        EMPTY: _set_empty,
    }

    def find_and_change_type_of_cell(self, cell_ind: tuple[int, int], new_type: str) -> List[Cell] | None:
        handler = self._TYPE_HANDLERS.get(new_type)
        if handler is None:
            raise ValueError(f"Unbekannter Zelltyp: {new_type}")
        return handler(self, cell_ind)

    # -------------------------------------------------------------------------
    #  Pfadbereinigungen
    # -------------------------------------------------------------------------
    def clear_current_path_points(self) -> list[Cell]:
        temp = list(self.current_path_points)
        for cell in temp:
            self._set_seen_point(cell.get_cell_ind())
        self.current_path_points.clear()
        return temp

    def clear_board(self) -> None:
        for row in self.grid:
            for cell in row:
                self._remove_from_sets(cell)
                cell.set_cell_type(EMPTY)
                self._notify_change(cell)
        self.targets.clear()
        self.obstacles.clear()
        self.starting_points.clear()
        self.seen_points.clear()
        self.current_path_points.clear()
        self.way_points.clear()

    def clear_board_of_pathfinding_types(self) -> list[Cell]:
        removed = []
        for row in self.grid:
            for cell in row:
                if cell.cell_type in (SEEN_POINT, CURRENT_PATH_CELL, WAY_POINT):
                    if cell not in self.starting_points:
                        removed.append(cell)
                        self._set_empty(cell.get_cell_ind())
        self.seen_points.clear()
        self.current_path_points.clear()
        self.way_points.clear()
        return removed

    # -------------------------------------------------------------------------
    #  Nachbarschaft
    # -------------------------------------------------------------------------
    def get_adjacent_cells(self, cell: Cell) -> List[Cell] | None:
        row, col = cell.get_cell_ind()
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]
        neighbours = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.height and 0 <= nc < self.width:
                neighbours.append(self.grid[nr][nc])
        return neighbours or None

    def get_adjacent_non_obstacle_cells(self, cell: Cell) -> List[Cell] | None:
        neighbours = self.get_adjacent_cells(cell)
        if not neighbours:
            return None
        return [n for n in neighbours if n.cell_type != OBSTACLE]

    def get_cells_of_type(self, cell_type: str) -> list[Cell]:
        return [cell for row in self.grid for cell in row if cell.cell_type == cell_type]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    g = Grid(5, 5)
    g.find_and_change_type_of_cell((1, 1), OBSTACLE)
    assert g.grid[1][1].cell_type == OBSTACLE
    g.find_and_change_type_of_cell((2, 2), TARGET)
    assert len(g.targets) == 1
    g.find_and_change_type_of_cell((2, 2), EMPTY)
    assert len(g.targets) == 0
    print("Grid tests passed.")