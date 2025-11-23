import pygame
import time
from typing import Sequence

from constants import *
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder
from drawing_grid import DrawingGrid
from sensor_data import simulate_lidar_scan


class DrawingBoard:
    def __init__(self, **drawing_grids: DrawingGrid) -> None:
        self.drawing_grids = drawing_grids
        
        self.reset_pathfinder()
        
        self.initialise_canvas()
        
    def initialise_canvas(self) -> None:
        #lets pygame initialise and makes it usebale
        pygame.init()

        pygame.font.init()  # you have to call this at the start, 
                            # if you want to use this module.
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        
        #lets the program detect a mouse press
        self.MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
        self.MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
        self.MOUSEMOTION = pygame.MOUSEMOTION
        self.mouse = pygame.mouse.get_pressed()
        
        # Create a custom event ID
        self.TEN_MILLISECOND_TIMEOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TEN_MILLISECOND_TIMEOUT, 10)  # every 10ms = 0.01 seconds
        
        #shows screen
        screen_width = 0
        screen_height = 0
        for dg in self.drawing_grids.values():
            size = dg.get_screen_dimensions()
            screen_width = max(size[0], screen_width)
            screen_height = max(size[1], screen_height)            
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        
        #makes how fast it updates in ms
        self.clock = pygame.time.Clock()

        #sets title
        pygame.display.set_caption("PATHFINDER")
        
    
    def draw_boards(self):
        for dg in self.drawing_grids.values():
            dg.draw_board(self.screen)
            
    def clear_board(self, grid_name: str):
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].clear_board()
            self.drawing_grids[grid_name].draw_board(self.screen)
            
    def clear_boards(self):
        for dg in self.drawing_grids.values():
            dg.clear_board()
            dg.draw_board(self.screen)
            
    def create_random_maze(self, grid_name: str):
        if grid_name in self.drawing_grids:
            self.drawing_grids[grid_name].create_random_maze()
            self.drawing_grids[grid_name].draw_board(self.screen)
            
    def find_board_hit(self, pos: tuple) -> tuple[str, tuple]|None:
        for grid_name, dg in self.drawing_grids.items():
            if grid_name not in [MAIN_GRID]:
                continue
            
            cell_ind = dg.find_cell_hit(pos)
            if cell_ind[0] != -1 and cell_ind[1] != -1:
                return grid_name, cell_ind
        return None
    
    def clear_current_path(self, grid_name: str):
        removed_cells = self.drawing_grids[grid_name].grid.clear_current_path_points()
        for r_c in removed_cells:
            # print("removed path cell:", r_c)
            self.drawing_grids[grid_name].grid.find_and_change_type_of_cell(r_c.get_cell_ind(), SEEN_POINT)
            pos_cell = self.drawing_grids[grid_name].get_pos_of_cell(r_c.get_cell_ind())
            if pos_cell:
                self.drawing_grids[grid_name].draw_cell(self.screen, r_c,
                                                    pos_cell[0], pos_cell[1],
                                                    self.drawing_grids[grid_name].length_squares,
                                                    self.drawing_grids[grid_name].length_squares)
            else:
                print("Could not get position of cell in previous path:", r_c, "in pathfinder step")
                
    def reset_pathfinder(self):
        self.pf = None  # Reset Pathfinder for next run
        self.find_gen = None
    
    def pathfind_step_by_step(self, show_current_path: bool = False):
        if self.pf is None or self.find_gen is None:
            self.pf = Pathfinder(self.drawing_grids[MAIN_GRID].grid)
            self.find_gen = self.pf.find(A_STAR)
        
        try:
            if self.find_gen:
                changed_cells, current_cell = next(self.find_gen)
                
                if changed_cells:
                    for c_c in changed_cells:
                        pos_cell = self.drawing_grids[MAIN_GRID].get_pos_of_cell(c_c.get_cell_ind())
                        if pos_cell:
                            self.drawing_grids[MAIN_GRID].draw_cell(self.screen, c_c,
                                                                 pos_cell[0], pos_cell[1],
                                                                 self.drawing_grids[MAIN_GRID].length_squares,
                                                                 self.drawing_grids[MAIN_GRID].length_squares)
                        else:
                            print("Could not get position of cell:", c_c, "in pathfinder step")
                    
                    if show_current_path:
                        self.clear_current_path(MAIN_GRID)
                                
                        current_cell_path = self.pf.get_parents(current_cell) if current_cell else []
                        for c_p in current_cell_path:
                            # print("current path cell:", c_p)
                            self.drawing_grids[MAIN_GRID].grid.find_and_change_type_of_cell(c_p.get_cell_ind(), CURRENT_PATH_CELL)
                            pos_cell = self.drawing_grids[MAIN_GRID].get_pos_of_cell(c_p.get_cell_ind())
                            if pos_cell:
                                self.drawing_grids[MAIN_GRID].draw_cell(self.screen, c_p,
                                                                    pos_cell[0], pos_cell[1],
                                                                    self.drawing_grids[MAIN_GRID].length_squares,
                                                                    self.drawing_grids[MAIN_GRID].length_squares)
                            else:
                                print("Could not get position of cell in current path:", c_p, "in pathfinder step")
                                
                return False
        except StopIteration:
            cells = None   
            self.reset_pathfinder()

            return True
        except Exception as e:
            print("Error during pathfinding step:", e)
            self.reset_pathfinder()
            return True
        
    def show_sensor_data(self):
        self.clear_board(SENSOR_GRID)
        if self.drawing_grids[MAIN_GRID].grid.starting_points:
            start_cell = self.drawing_grids[MAIN_GRID].grid.starting_points[0]
            free_cells, occupied_cells = simulate_lidar_scan(self.drawing_grids[MAIN_GRID].grid, start_cell.get_cell_ind(), 
                                                                scan_range=20, points_per_rotation=180)
            # print("LIDAR Scan from", start_cell.get_cell_ind())
            # print("Free cells detected by LIDAR: ", free_cells)
            # print("Occupied cells detected by LIDAR: ", occupied_cells)
            
            for free_cell in free_cells:
                self.drawing_grids[SENSOR_GRID].change_type_of_cell(self.screen, free_cell, EXPECTED_FREE)
            for occupied_cell in occupied_cells:
                self.drawing_grids[SENSOR_GRID].change_type_of_cell(self.screen, occupied_cell, EXPECTED_OCCUPIED)
            self.drawing_grids[SENSOR_GRID].change_type_of_cell(self.screen, start_cell.get_cell_ind(), ROVER_POSITION)
        else:
            # print("No starting point set for LIDAR scan.")
            pass

    def mainloop(self):
        
        self.draw_boards()
        
        left_click_button_down = False
        running = True
        pathfind_mode = False
        pathfind_finished = False
        show_current_path = False
        
        #main loop
        while running:                             
            # --- Main event loop
            #checks every event
            for event in pygame.event.get():
                #gets position of the mouse
                pos_mouse = pygame.mouse.get_pos()
                #checks if you close the page
                if event.type == pygame.QUIT:
                    #quits main loop
                    running = False
                    
                elif event.type == self.TEN_MILLISECOND_TIMEOUT and pathfind_mode and not pathfind_finished and not show_current_path:
                    if self.pathfind_step_by_step():
                        print("pathfinder finished")
                        pathfind_finished = True
                
                #checks key presses
                elif event.type == pygame.KEYDOWN:
                    #checks for return key
                    if event.key == pygame.K_RETURN:
                        pathfind_mode = not pathfind_mode
                        print("Pathfinding mode:", pathfind_mode)

                    elif event.key == pygame.K_SPACE and not pathfind_mode: 
                        self.reset_pathfinder()                           
                        self.clear_boards()
                        pathfind_finished = False
                    
                    elif event.key == pygame.K_c and not pathfind_mode:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit 
                            self.clear_board(grid_name)
                        
                    elif event.key == pygame.K_p and not pathfind_mode:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit 
                            self.drawing_grids[grid_name].find_and_change_type_of_cell(self.screen, pos_mouse, TARGET)
                                
                    elif event.key == pygame.K_m and not pathfind_mode:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit 
                            self.create_random_maze(grid_name)
                            self.reset_pathfinder()                           
                            self.draw_boards()
                            
                            if grid_name == MAIN_GRID:
                                self.show_sensor_data()
                                
                            pathfind_finished = False
                                
                    elif event.key == pygame.K_i:
                        print("--------------Debugging Info--------------------")
                        print("Starting Points:", self.drawing_grids[MAIN_GRID].grid.starting_points)
                        print("Targets:", self.drawing_grids[MAIN_GRID].grid.targets)
                        print("Obstacles:", self.drawing_grids[MAIN_GRID].grid.obstacles)
                        print("--------------Pathfinder Info-------------------")
                        print("Seen Points:", self.drawing_grids[MAIN_GRID].grid.seen_points)
                        print("Way Points:", self.drawing_grids[MAIN_GRID].grid.way_points)
                        print("------------------------------------------------")
                        print()
                        print()
                        
                    elif event.key == pygame.K_j and pathfind_mode and not pathfind_finished:
                        self.clear_current_path(MAIN_GRID)
                        show_current_path = not show_current_path
                        if self.pathfind_step_by_step(show_current_path=show_current_path):
                            print("pathfinder finished")
                            pathfind_finished = True
                        
                    elif event.key == pygame.K_s and not pathfind_mode:
                        self.show_sensor_data()
                                    
                elif event.type == self.MOUSEBUTTONDOWN and not pathfind_mode:
                    if event.button == 1:     
                        left_click_button_down=True   
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit                     
                            self.drawing_grids[grid_name].find_and_change_type_of_cell(self.screen, pos_mouse, OBSTACLE)
                            if grid_name == MAIN_GRID:
                                self.show_sensor_data()

                    if event.button == 2:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit 
                            self.drawing_grids[grid_name].find_and_change_type_of_cell(self.screen, pos_mouse, EMPTY)
                            if grid_name == MAIN_GRID:
                                self.show_sensor_data()

                    if event.button == 3:
                        board_hit = self.find_board_hit(pos_mouse)
                        if board_hit:
                            grid_name, cell_ind = board_hit 
                            self.drawing_grids[grid_name].find_and_change_type_of_cell(self.screen, pos_mouse, STARTING_POINT)
                            if grid_name == MAIN_GRID:
                                self.show_sensor_data()
                
                elif event.type == self.MOUSEBUTTONUP and not pathfind_mode:
                    left_click_button_down=False

                if event.type == self.MOUSEMOTION and left_click_button_down==True and not pathfind_mode:
                    board_hit = self.find_board_hit(pos_mouse)
                    if board_hit:
                        grid_name, cell_ind = board_hit 
                        self.drawing_grids[grid_name].find_and_change_type_of_cell(self.screen, pos_mouse, OBSTACLE)
                        if grid_name == MAIN_GRID:
                            if grid_name == MAIN_GRID:
                                self.show_sensor_data()
                
                                        
            #sets time of the page updating             
            self.clock.tick(100)

            #shows the progress on screen
            pygame.display.flip()

        #when the main loop is interrupted the programm quits
        pygame.quit()
        
        
if __name__ == "__main__":
    print("This is the drawing board module")
