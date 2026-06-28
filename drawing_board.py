# drawing_board.py
import pygame
import time
from typing import Sequence

from constants import *
from cell import Cell
from grid import Grid

from pathfinder import Pathfinder
from drawing_grid import DrawingGrid


class DrawingBoard:
    def __init__(self, **drawing_grids: DrawingGrid) -> None:
        self.drawing_grids = drawing_grids
        
        self.saved_boards_folder = "saved_boards"
        
        self.reset_pathfinder_vars()
        
        self.initialise_canvas()
        
    def initialise_canvas(self) -> None:
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        
        self.MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
        self.MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
        self.MOUSEMOTION = pygame.MOUSEMOTION
        self.mouse = pygame.mouse.get_pressed()
        
        self.TEN_MILLISECOND_TIMEOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TEN_MILLISECOND_TIMEOUT, 10)
        
        screen_width = 0
        screen_height = 0
        for dg in self.drawing_grids.values():
            size = dg.get_screen_dimensions()
            screen_width = max(size[0], screen_width)
            screen_height = max(size[1], screen_height)            
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("PATHFINDER")
    
    def save_board(self, grid_name: str, filename: str) -> None:
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].save_board(f"{self.saved_boards_folder}/{filename}")
            
    def load_board(self, grid_name: str, filename: str) -> None:
        if grid_name in self.drawing_grids:            
            self.drawing_grids[grid_name].load_board(f"{self.saved_boards_folder}/{filename}")
            self.drawing_grids[grid_name].draw_board(self.screen)
    
    def draw_boards(self):
        for dg in self.drawing_grids.values():
            dg.draw_board(self.screen)
            
    def clear_board(self, grid_name: str):
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].clear_board(self.screen)
            
    def clear_boards(self):
        for dg in self.drawing_grids.values():
            self.clear_board(dg.grid.grid_name)
            
    def create_random_maze(self, grid_name: str):
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].create_random_maze()
            self.drawing_grids[grid_name].draw_board(self.screen)
                
    def find_board_hit(self, pos: tuple) -> tuple[str, tuple] | None:
        for grid_name, dg in self.drawing_grids.items():
            if grid_name not in [MAIN_GRID]:
                continue
            cell_ind = dg.find_cell_hit(pos)
            if cell_ind[0] != -1 and cell_ind[1] != -1:
                return grid_name, cell_ind
        return None
                
    def reset_pathfinder_vars(self):
        self.pf = None
        self.find_gen = None
        
    def reset_pathfinder(self):
        self.reset_pathfinder_vars()
        self.drawing_grids[ROVER_GRID].clear_board_of_pathfinding_types(self.screen)
    
    def pathfind_step_by_step(self, show_current_path: bool = False, batch_size: int = 10):
        if self.pf is None or self.find_gen is None:
            self.pf = Pathfinder(self.drawing_grids[ROVER_GRID].grid)
            self.find_gen = self.pf.find(A_STAR)

        all_changed_cells = set()
        last_cell = None

        for _ in range(batch_size):
            try:
                if self.find_gen:
                    changed_cells, current_cell = next(self.find_gen)
                    if changed_cells:
                        all_changed_cells.update(changed_cells)
                        last_cell = current_cell
            except StopIteration:
                self.reset_pathfinder_vars()
                return True   # fertig
            except Exception as e:
                print("Error during pathfinding step:", e)
                self.reset_pathfinder_vars()
                return True

        if all_changed_cells:
            for c_c in all_changed_cells:
                self.drawing_grids[ROVER_GRID].update_cell_on_screen(self.screen, c_c)
            if last_cell:
                self.show_sensor_data(start_point_cell=last_cell)

            if show_current_path and last_cell:
                self.drawing_grids[ROVER_GRID].clear_current_path(self.screen)
                current_cell_path = self.pf.get_parents(last_cell)
                for c_p in current_cell_path:
                    self.drawing_grids[ROVER_GRID].change_type_of_cell(
                        self.screen, c_p.get_cell_ind(), CURRENT_PATH_CELL
                    )
        return False
        
    def show_sensor_data(self, start_point_cell: Cell | None = None) -> None:
        if start_point_cell is None and self.drawing_grids[ROVER_GRID].grid.starting_points:
            start_cell = next(iter(self.drawing_grids[ROVER_GRID].grid.starting_points))
            self.drawing_grids[SENSOR_GRID].show_sensor_data(self.screen,
                                                             self.drawing_grids[ROVER_GRID].grid,
                                                             start_cell)
        elif start_point_cell:
            self.drawing_grids[SENSOR_GRID].show_sensor_data(self.screen,
                                                             self.drawing_grids[ROVER_GRID].grid,
                                                             start_point_cell)

    def mainloop(self):
        self.draw_boards()
        pygame.display.flip()

        left_click_button_down = False
        running = True
        pathfind_mode = False
        pathfind_finished = False
        show_current_path = False
        start_time = None
        end_time = None

        while running:
            needs_flip = False

            for event in pygame.event.get():
                pos_mouse = pygame.mouse.get_pos()

                if event.type == pygame.QUIT:
                    running = False

                elif event.type == self.TEN_MILLISECOND_TIMEOUT and pathfind_mode and not pathfind_finished and not show_current_path:
                    finished = self.pathfind_step_by_step(batch_size=20)
                    if finished:
                        print("pathfinder finished")
                        pathfind_finished = True
                        end_time = time.time()
                        self.draw_boards()
                        if start_time is not None:
                            print(f"Pathfinding took {end_time - start_time:.4f} seconds")
                    needs_flip = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pathfind_mode = not pathfind_mode
                        print("Pathfinding mode:", pathfind_mode)
                        if pathfind_mode:
                            start_time = time.time()
                        needs_flip = True

                    elif event.key == pygame.K_SPACE and not pathfind_mode:
                        self.reset_pathfinder_vars()
                        self.clear_boards()
                        pathfind_finished = False
                        needs_flip = True

                    elif event.key == pygame.K_c and not pathfind_mode:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit
                            self.clear_board(grid_name)
                            needs_flip = True

                    elif event.key == pygame.K_p and not pathfind_mode:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit
                            cell_ind = self.drawing_grids[grid_name].change_type_of_cell(self.screen, cell_ind, TARGET)
                            self.drawing_grids[ROVER_GRID].change_type_of_cell(self.screen, cell_ind, TARGET)
                            needs_flip = True

                    elif event.key == pygame.K_m and not pathfind_mode:
                        self.create_random_maze(ROVER_GRID)
                        self.clear_board(SENSOR_GRID)
                        self.reset_pathfinder_vars()
                        self.draw_boards()
                        self.show_sensor_data()
                        pathfind_finished = False
                        needs_flip = True

                    elif event.key == pygame.K_i:
                        print("--------------Debugging Info--------------------")
                        print("Starting Points:", self.drawing_grids[ROVER_GRID].grid.starting_points)
                        print("Targets:", self.drawing_grids[ROVER_GRID].grid.targets)
                        print("Obstacles:", self.drawing_grids[ROVER_GRID].grid.obstacles)
                        print("--------------Pathfinder Info-------------------")
                        print("Seen Points:", self.drawing_grids[ROVER_GRID].grid.seen_points)
                        print("Way Points:", self.drawing_grids[ROVER_GRID].grid.way_points)
                        print("------------------------------------------------")
                        print()

                    elif event.key == pygame.K_j and pathfind_mode and not pathfind_finished:
                        self.drawing_grids[ROVER_GRID].clear_current_path(self.screen)
                        show_current_path = not show_current_path
                        if self.pathfind_step_by_step(show_current_path=show_current_path, batch_size=20):
                            print("pathfinder finished")
                            pathfind_finished = True
                        needs_flip = True

                    elif event.key == pygame.K_r and not pathfind_mode:
                        self.reset_pathfinder()
                        needs_flip = True

                    elif event.key == pygame.K_s and not pathfind_mode:
                        self.save_board(MAIN_GRID, "rover_grid.txt")

                    elif event.key == pygame.K_l and not pathfind_mode:
                        self.load_board(ROVER_GRID, "rover_grid.txt")
                        self.load_board(MAIN_GRID, "rover_grid.txt")
                        needs_flip = True

                    elif event.key == pygame.K_1 and not pathfind_mode:
                        print("Loading board 1")
                        self.load_board(ROVER_GRID, "1.txt")
                        self.load_board(MAIN_GRID, "1.txt")
                        self.show_sensor_data()
                        needs_flip = True

                    elif event.key == pygame.K_2 and not pathfind_mode:
                        print("Loading board 2")
                        self.load_board(ROVER_GRID, "2.txt")
                        self.load_board(MAIN_GRID, "2.txt")
                        self.show_sensor_data()
                        needs_flip = True

                    elif event.key == pygame.K_3 and not pathfind_mode:
                        print("Loading board 3")
                        self.load_board(ROVER_GRID, "3.txt")
                        self.load_board(MAIN_GRID, "3.txt")
                        self.show_sensor_data()
                        needs_flip = True

                    elif event.key == pygame.K_4 and not pathfind_mode:
                        print("Loading board 4")
                        self.load_board(ROVER_GRID, "4.txt")
                        self.load_board(MAIN_GRID, "4.txt")
                        self.show_sensor_data()
                        needs_flip = True

                elif event.type == self.MOUSEBUTTONDOWN and not pathfind_mode:
                    if event.button == 1:
                        left_click_button_down = True
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit
                            self.drawing_grids[grid_name].change_type_of_cell(self.screen, cell_ind, OBSTACLE)
                            self.drawing_grids[ROVER_GRID].change_type_of_cell(self.screen, cell_ind, OBSTACLE)
                            if grid_name == MAIN_GRID:
                                self.clear_board(SENSOR_GRID)
                                self.show_sensor_data()
                            needs_flip = True

                    if event.button == 2:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit
                            self.drawing_grids[grid_name].change_type_of_cell(self.screen, cell_ind, EMPTY)
                            self.drawing_grids[ROVER_GRID].change_type_of_cell(self.screen, cell_ind, EMPTY)
                            if grid_name == MAIN_GRID:
                                self.clear_board(SENSOR_GRID)
                                self.show_sensor_data()
                            needs_flip = True

                    if event.button == 3:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit
                            self.drawing_grids[grid_name].change_type_of_cell(self.screen, cell_ind, STARTING_POINT)
                            self.drawing_grids[ROVER_GRID].change_type_of_cell(self.screen, cell_ind, STARTING_POINT)
                            if grid_name == MAIN_GRID:
                                self.clear_board(SENSOR_GRID)
                                self.show_sensor_data()
                            needs_flip = True

                elif event.type == self.MOUSEBUTTONUP and not pathfind_mode:
                    left_click_button_down = False

                if event.type == self.MOUSEMOTION and left_click_button_down and not pathfind_mode:
                    board_hit = self.find_board_hit(pos_mouse)
                    if board_hit:
                        grid_name, cell_ind = board_hit
                        self.drawing_grids[grid_name].change_type_of_cell(self.screen, cell_ind, OBSTACLE)
                        self.drawing_grids[ROVER_GRID].change_type_of_cell(self.screen, cell_ind, OBSTACLE)
                        if grid_name == MAIN_GRID:
                            self.clear_board(SENSOR_GRID)
                            self.show_sensor_data()
                        needs_flip = True

            if needs_flip:
                pygame.display.flip()

            self.clock.tick(100)