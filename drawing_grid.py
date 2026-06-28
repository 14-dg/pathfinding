"""
Visuelle Repräsentation eines Grids.
Kümmert sich um das Zeichnen und reagiert automatisch auf Grid-Änderungen.
"""

from __future__ import annotations
import logging
from random import randint
import pygame
from typing import Optional, Tuple

from cell import Cell
from grid import Grid
from constants import *
from sensor_data import simulate_lidar_scan

logger = logging.getLogger(__name__)


class DrawingGrid:
    def __init__(
        self,
        grid: Grid,
        length_square: int = 5,
        margin: int = 1,
        offset_x: int = 0,
        offset_y: int = 0,
    ) -> None:
        self.grid = grid
        self.length_squares = length_square
        self.margin = margin
        self.offset_x = offset_x
        self.offset_y = offset_y

        self.screen_width = (length_square + margin) * grid.width - margin
        self.screen_height = (length_square + margin) * grid.height - margin

        # Pygame-Screen (wird von attach_to_grid gesetzt)
        self.screen: Optional[pygame.Surface] = None

        # Cache für Zeichenrechtecke (cell -> (x,y,w,h))
        self._rect_map: dict[Cell, tuple[int, int, int, int]] = {}
        self._build_rect_map()

        # Automatische Aktualisierung nach Grid-Änderungen
        self.grid.add_change_listener(self._on_cell_changed)

    # -------------------------------------------------------------------------
    #  Zeichenvorbereitung
    # -------------------------------------------------------------------------
    def _build_rect_map(self) -> None:
        self._rect_map.clear()
        for row in range(self.grid.height):
            for col in range(self.grid.width):
                cell = self.grid.grid[row][col]
                x = self.offset_x + col * (self.length_squares + self.margin)
                y = self.offset_y + row * (self.length_squares + self.margin)
                self._rect_map[cell] = (x, y, self.length_squares, self.length_squares)

    # -------------------------------------------------------------------------
    #  Verbindung mit Pygame
    # -------------------------------------------------------------------------
    def attach_to_grid(self, screen: pygame.Surface) -> None:
        """Registriert den Screen, damit automatisch gezeichnet werden kann."""
        self.screen = screen

    def get_screen_dimensions(self) -> tuple[int, int]:
        return (self.screen_width + self.offset_x, self.screen_height + self.offset_y)

    # -------------------------------------------------------------------------
    #  Zeichenmethoden
    # -------------------------------------------------------------------------
    def _draw_cell(self, cell: Cell) -> None:
        if self.screen is None:
            logger.warning("Kein Screen zugewiesen.")
            return
        x, y, w, h = self._rect_map[cell]
        pygame.draw.rect(self.screen, cell.color, (x, y, w, h))

    def _on_cell_changed(self, cell: Cell) -> None:
        """Callback vom Grid – zeichnet nur die geänderte Zelle neu."""
        if self.screen:
            self._draw_cell(cell)

    def draw_board(self) -> None:
        """Zeichnet das gesamte Board."""
        if self.screen is None:
            return
        for cell in self._rect_map:
            self._draw_cell(cell)

    # -------------------------------------------------------------------------
    #  Öffentliche Aktionen
    # -------------------------------------------------------------------------
    def find_cell_hit(self, pos: tuple[int, int]) -> tuple[int, int]:
        pos_x, pos_y = pos
        cell_x = (pos_x - self.offset_x) / (self.length_squares + self.margin)
        cell_y = (pos_y - self.offset_y) / (self.length_squares + self.margin)
        col = int(round(cell_x))
        row = int(round(cell_y))
        if col < 0 or col >= self.grid.width or row < 0 or row >= self.grid.height:
            return (-1, -1)
        return (row, col)

    def change_type_of_cell(self, cell_ind: tuple[int, int], cell_type: str) -> None:
        self.grid.find_and_change_type_of_cell(cell_ind, cell_type)

    def clear_board(self) -> None:
        self.grid.clear_board()
        self.draw_board()

    def clear_board_of_pathfinding_types(self) -> None:
        self.grid.clear_board_of_pathfinding_types()
        self.draw_board()

    def clear_current_path(self) -> None:
        removed = self.grid.clear_current_path_points()
        for cell in removed:
            self._draw_cell(cell)

    def create_random_maze(self) -> None:
        for row in self.grid.grid:
            for cell in row:
                if randint(1, 100) <= MAZE_EMPTY_PROBABILITY:
                    self.grid.find_and_change_type_of_cell(cell.get_cell_ind(), EMPTY)
                else:
                    self.grid.find_and_change_type_of_cell(cell.get_cell_ind(), OBSTACLE)

        target_cell = self.grid.grid[
            int(MAZE_TARGET_ROW_FACTOR * self.grid.height)
        ][int(MAZE_TARGET_COL_FACTOR * self.grid.height)]
        start_cell = self.grid.grid[
            int(MAZE_START_ROW_FACTOR * self.grid.height)
        ][int(MAZE_START_COL_FACTOR * self.grid.width)]
        self.grid.find_and_change_type_of_cell(target_cell.get_cell_ind(), TARGET)
        self.grid.find_and_change_type_of_cell(start_cell.get_cell_ind(), STARTING_POINT)

    def show_sensor_data(self, rover_grid: Grid, start_cell: Cell) -> None:
        free, occupied = simulate_lidar_scan(rover_grid, start_cell.get_cell_ind())
        for fc in free:
            self.grid.find_and_change_type_of_cell(fc, EXPECTED_FREE)
        for oc in occupied:
            self.grid.find_and_change_type_of_cell(oc, EXPECTED_OCCUPIED)
        self.grid.find_and_change_type_of_cell(start_cell.get_cell_ind(), ROVER_POSITION)

    # -------------------------------------------------------------------------
    #  Persistenz
    # -------------------------------------------------------------------------
    def save_board(self, filename: str) -> None:
        self.grid.save_grid(filename)

    def load_board(self, filename: str) -> None:
        self.grid.load_grid(filename)
        self._build_rect_map()
        logger.info(f"Geladen: {filename}")


if __name__ == "__main__":
    # Kein Pygame-Test hier, weil kein Screen initialisiert wird.
    print("DrawingGrid – manuelle Tests sind nur mit Pygame möglich.")