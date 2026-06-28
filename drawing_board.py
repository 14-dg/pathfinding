"""
Hauptsteuerung der Anwendung.
Verwaltet Fenster, Events und koordiniert die Grids.
"""

from __future__ import annotations
import logging
import time
from typing import Optional, Callable

import pygame

from constants import *
from cell import Cell
from pathfinder import Pathfinder
from drawing_grid import DrawingGrid

logger = logging.getLogger(__name__)


class DrawingBoard:
    def __init__(self, **drawing_grids: DrawingGrid) -> None:
        self.drawing_grids: dict[str, DrawingGrid] = drawing_grids
        self.saved_boards_folder = "saved_boards"

        self._pf: Optional[Pathfinder] = None
        self._find_gen = None
        self._last_step_cell: Optional[Cell] = None

        self._left_button_down = False
        self._pathfind_mode = False
        self._pathfind_finished = False
        self._show_current_path = False
        self._start_time: Optional[float] = None
        self._end_time: Optional[float] = None
        self._needs_flip = False

        self._init_pygame()
        self._attach_grids()

    # -------------------------------------------------------------------------
    #  Pygame-Initialisierung
    # -------------------------------------------------------------------------
    def _init_pygame(self) -> None:
        pygame.init()
        pygame.font.init()

        self.MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
        self.MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
        self.MOUSEMOTION = pygame.MOUSEMOTION

        self.TEN_MILLISECOND_TIMEOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TEN_MILLISECOND_TIMEOUT, TIMER_INTERVAL_MS)

        screen_width = 0
        screen_height = 0
        for dg in self.drawing_grids.values():
            w, h = dg.get_screen_dimensions()
            screen_width = max(screen_width, w)
            screen_height = max(screen_height, h)
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PATHFINDER")

    def _attach_grids(self) -> None:
        for dg in self.drawing_grids.values():
            dg.attach_to_grid(self.screen)

    # -------------------------------------------------------------------------
    #  Persistenz
    # -------------------------------------------------------------------------
    def save_board(self, grid_name: str, filename: str) -> None:
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].save_board(f"{self.saved_boards_folder}/{filename}")

    def load_board(self, grid_name: str, filename: str) -> None:
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].load_board(f"{self.saved_boards_folder}/{filename}")

    # -------------------------------------------------------------------------
    #  Pfadfinder-Hilfen
    # -------------------------------------------------------------------------
    def _reset_pathfinder_vars(self) -> None:
        self._pf = None
        self._find_gen = None
        self._last_step_cell = None

    def _reset_pathfinder(self) -> None:
        self._reset_pathfinder_vars()
        self.drawing_grids[ROVER_GRID].clear_board_of_pathfinding_types()

    def _pathfind_step(self, show_path: bool = False, batch: int = PATHFINDING_BATCH_SIZE) -> bool:
        if self._pf is None or self._find_gen is None:
            self._pf = Pathfinder(self.drawing_grids[ROVER_GRID].grid)
            self._find_gen = self._pf.find(A_STAR)

        all_changed: set[Cell] = set()
        last_cell = None

        for _ in range(batch):
            try:
                if self._find_gen:
                    changed, current = next(self._find_gen)
                    if changed:
                        all_changed.update(changed)
                        last_cell = current
            except StopIteration:
                self._reset_pathfinder_vars()
                return True
            except Exception as e:
                logger.exception("Fehler im Pfadfinder-Schritt")
                self._reset_pathfinder_vars()
                return True

        self._last_step_cell = last_cell

        if all_changed:
            if last_cell:
                self._show_sensor_data(last_cell)
            if show_path and last_cell and self._pf:
                self.drawing_grids[ROVER_GRID].clear_current_path()
                path_cells = self._pf.get_parents(last_cell)
                for pc in path_cells:
                    self.drawing_grids[ROVER_GRID].change_type_of_cell(pc.get_cell_ind(), CURRENT_PATH_CELL)

        return False

    # -------------------------------------------------------------------------
    #  Sensor-Anzeige
    # -------------------------------------------------------------------------
    def _show_sensor_data(self, start_cell: Cell | None = None) -> None:
        if start_cell is None:
            if self.drawing_grids[ROVER_GRID].grid.starting_points:
                start_cell = next(iter(self.drawing_grids[ROVER_GRID].grid.starting_points))
            else:
                return
        self.drawing_grids[SENSOR_GRID].show_sensor_data(
            self.drawing_grids[ROVER_GRID].grid, start_cell
        )

    # -------------------------------------------------------------------------
    #  Maus-Hit-Test
    # -------------------------------------------------------------------------
    def _find_board_hit(self, pos: tuple[int, int]) -> tuple[str, tuple[int, int]] | None:
        for name, dg in self.drawing_grids.items():
            if name != MAIN_GRID:
                continue
            row, col = dg.find_cell_hit(pos)
            if row != -1 and col != -1:
                return name, (row, col)
        return None

    # -------------------------------------------------------------------------
    #  Event-Handler
    # -------------------------------------------------------------------------
    def _handle_quit(self, event: pygame.event.Event) -> bool:
        return False

    def _handle_timer(self, event: pygame.event.Event) -> bool:
        if not (self._pathfind_mode and not self._pathfind_finished and not self._show_current_path):
            return True
        finished = self._pathfind_step(batch=PATHFINDING_BATCH_SIZE)
        if finished:
            logger.info("Pfadfinder beendet.")
            self._pathfind_finished = True
            self._end_time = time.time()
            self._draw_all()
            if self._start_time is not None:
                print(f"Pathfinding took {self._end_time - self._start_time:.4f} seconds")
        self._needs_flip = True
        return True

    def _handle_keydown(self, event: pygame.event.Event) -> bool:
        key_actions: dict[int, Callable[[], None]] = {
            pygame.K_RETURN: self._toggle_pathfinding,
            pygame.K_SPACE: self._clear_all,
            pygame.K_c: self._clear_grid_under_mouse,
            pygame.K_p: self._set_target,
            pygame.K_m: self._generate_maze,
            pygame.K_i: self._print_debug_info,
            pygame.K_j: self._toggle_current_path,
            pygame.K_r: self._reset_pathfinder,
            pygame.K_s: self._save,
            pygame.K_l: self._load_default,
            pygame.K_1: lambda: self._load_board(1),
            pygame.K_2: lambda: self._load_board(2),
            pygame.K_3: lambda: self._load_board(3),
            pygame.K_4: lambda: self._load_board(4),
        }
        action = key_actions.get(event.key)
        if action:
            action()
            self._needs_flip = True
        return True

    def _handle_mouse_down(self, event: pygame.event.Event) -> bool:
        if self._pathfind_mode:
            return True
        pos = pygame.mouse.get_pos()
        board_hit = self._find_board_hit(pos)
        if not board_hit:
            return True
        grid_name, cell_ind = board_hit

        if event.button == 1:
            self._left_button_down = True
            self._modify_cell(grid_name, cell_ind, OBSTACLE)
        elif event.button == 2:
            self._modify_cell(grid_name, cell_ind, EMPTY)
        elif event.button == 3:
            self._modify_cell(grid_name, cell_ind, STARTING_POINT)
        self._needs_flip = True
        return True

    def _handle_mouse_up(self, event: pygame.event.Event) -> bool:
        if event.button == 1:
            self._left_button_down = False
        return True

    def _handle_motion(self, event: pygame.event.Event) -> bool:
        if not self._left_button_down or self._pathfind_mode:
            return True
        pos = pygame.mouse.get_pos()
        board_hit = self._find_board_hit(pos)
        if board_hit:
            grid_name, cell_ind = board_hit
            self._modify_cell(grid_name, cell_ind, OBSTACLE)
            self._needs_flip = True
        return True

    # -------------------------------------------------------------------------
    #  Aktionen
    # -------------------------------------------------------------------------
    def _modify_cell(self, grid_name: str, cell_ind: tuple[int, int], new_type: str) -> None:
        self.drawing_grids[grid_name].change_type_of_cell(cell_ind, new_type)
        if grid_name == MAIN_GRID:
            self.drawing_grids[ROVER_GRID].change_type_of_cell(cell_ind, new_type)
            self._show_sensor_data()

    def _toggle_pathfinding(self) -> None:
        self._pathfind_mode = not self._pathfind_mode
        logger.info(f"Pathfind mode: {self._pathfind_mode}")
        if self._pathfind_mode:
            self._start_time = time.time()
        self._needs_flip = True

    def _clear_all(self) -> None:
        self._reset_pathfinder_vars()
        for dg in self.drawing_grids.values():
            dg.clear_board()
        self._pathfind_finished = False

    def _clear_grid_under_mouse(self) -> None:
        hit = self._find_board_hit(pygame.mouse.get_pos())
        if hit:
            self.drawing_grids[hit[0]].clear_board()

    def _set_target(self) -> None:
        hit = self._find_board_hit(pygame.mouse.get_pos())
        if hit:
            grid_name, cell_ind = hit
            self.drawing_grids[grid_name].change_type_of_cell(cell_ind, TARGET)
            self.drawing_grids[ROVER_GRID].change_type_of_cell(cell_ind, TARGET)

    def _generate_maze(self) -> None:
        self.drawing_grids[ROVER_GRID].create_random_maze()
        self.drawing_grids[SENSOR_GRID].clear_board()
        self._reset_pathfinder_vars()
        self._draw_all()
        self._show_sensor_data()
        self._pathfind_finished = False

    def _print_debug_info(self) -> None:
        rover = self.drawing_grids[ROVER_GRID].grid
        print("--------------Debugging Info--------------------")
        print("Starting Points:", rover.starting_points)
        print("Targets:", rover.targets)
        print("Obstacles:", rover.obstacles)
        print("--------------Pathfinder Info-------------------")
        print("Seen Points:", rover.seen_points)
        print("Way Points:", rover.way_points)
        print("------------------------------------------------\n")

    def _toggle_current_path(self) -> None:
        if self._pathfind_mode and not self._pathfind_finished:
            self._show_current_path = not self._show_current_path
            self.drawing_grids[ROVER_GRID].clear_current_path()
            if self._show_current_path and self._last_step_cell and self._pf:
                path_cells = self._pf.get_parents(self._last_step_cell)
                for pc in path_cells:
                    self.drawing_grids[ROVER_GRID].change_type_of_cell(pc.get_cell_ind(), CURRENT_PATH_CELL)

    def _save(self) -> None:
        self.save_board(MAIN_GRID, "rover_grid.txt")

    def _load_default(self) -> None:
        self.load_board(ROVER_GRID, "rover_grid.txt")
        self.load_board(MAIN_GRID, "rover_grid.txt")
        self._draw_all()
        self._show_sensor_data()

    def _load_board(self, number: int) -> None:
        filename = f"{number}.txt"
        logger.info(f"Lade Board {number}")
        self.load_board(ROVER_GRID, filename)
        self.load_board(MAIN_GRID, filename)
        self._draw_all()
        self._show_sensor_data()

    # -------------------------------------------------------------------------
    #  Zeichenhilfen
    # -------------------------------------------------------------------------
    def _draw_all(self) -> None:
        for dg in self.drawing_grids.values():
            dg.draw_board()

    # -------------------------------------------------------------------------
    #  Hauptschleife
    # -------------------------------------------------------------------------
    def mainloop(self) -> None:
        self._draw_all()
        pygame.display.flip()

        running = True

        event_handlers: dict[int, Callable[[pygame.event.Event], bool]] = {
            pygame.QUIT:              self._handle_quit,
            self.TEN_MILLISECOND_TIMEOUT: self._handle_timer,
            pygame.KEYDOWN:           self._handle_keydown,
            pygame.MOUSEBUTTONDOWN:   self._handle_mouse_down,
            pygame.MOUSEBUTTONUP:     self._handle_mouse_up,
        }

        while running:
            self._needs_flip = False

            for event in pygame.event.get():
                handler = event_handlers.get(event.type)
                if handler is not None:
                    if not handler(event):
                        running = False
                        break
                if event.type == pygame.MOUSEMOTION:
                    self._handle_motion(event)

            if self._needs_flip:
                pygame.display.flip()
            self.clock.tick(FPS)


if __name__ == "__main__":
    print("DrawingBoard – wird über main.py gestartet.")