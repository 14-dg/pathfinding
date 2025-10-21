import pygame
import time

from constants import *
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder


class DrawingBoard:
    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.pf = None
        
        self.initialise_canvas()
        
    def initialise_canvas(self):
        #lets pygame initialate and makes it usebale
        pygame.init()

        pygame.font.init()  # you have to call this at the start, 
                            # if you want to use this module.
        self.myfont = pygame.font.SysFont('Comic Sans MS', 50)
        
        #lets the peogramm detect a mouse press
        self.MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
        self.MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
        self.MOUSEMOTION = pygame.MOUSEMOTION
        self.mouse = pygame.mouse.get_pressed()
        
        # Create a custom event ID
        self.TEN_MILLISECOND_TIMEOUT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.TEN_MILLISECOND_TIMEOUT, 10)  # every 10ms = 0.01 seconds
        
        #shows screen
        self.screen = pygame.display.set_mode(self.grid.get_screen_dimensions())
        
        #makes how fast it updates in ms
        self.clock = pygame.time.Clock()

        #sets title
        pygame.display.set_caption("PATHFINDER")

        
    def draw_cell(self, c: Cell) -> None:
        pygame.draw.rect(self.screen , c.color, (c.x, c.y, c.w, c.h))
    
    def draw_board(self):
        for h in self.grid.grid:
            for c in h:
                self.draw_cell(c)
                
    def reset_pathfinder(self):
        self.pf = None  # Reset Pathfinder for next run
        self.find_gen = None
    
    def pathfind_step_by_step(self):
        if not self.pf:
            self.pf = Pathfinder(self.grid)
            self.find_gen = self.pf.find(DIJKSTRA)
        
        
        try:
            if self.find_gen:
                cells = next(self.find_gen)
                # print("Step complete, changed cells:", len(cells))
                if cells:
                    for c in cells:
                        self.draw_cell(c)
        except StopIteration:
            cells = None   
            self.reset_pathfinder()

            return True
       
    def mainloop(self):
        
        self.draw_board()
        
        button_down = False
        running = True
        pathfind_mode = False
        pathfind_finished = False
        
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
                    
                elif event.type == self.TEN_MILLISECOND_TIMEOUT and pathfind_mode and not pathfind_finished:
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
                        self.grid.clear_board()
                        self.draw_board()
                        pathfind_finished = False
                        
                    elif event.key == pygame.K_p and not pathfind_mode:
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, TARGET)
                        if cells:
                            for target_cell in cells:
                                self.draw_cell(target_cell)
                                
                    elif event.key == pygame.K_c and not pathfind_mode:
                        self.grid.create_random_maze()
                        self.reset_pathfinder()                           
                        self.draw_board()
                        pathfind_finished = False
                                
                    elif event.key == pygame.K_s:
                        print("--------------Debugging Info--------------------")
                        print("Starting Points:", self.grid.starting_points)
                        print("Targets:", self.grid.targets)
                        print("Obstacles:", self.grid.obstacles)
                        print("--------------Pathfinder Info-------------------")
                        print("Seen Points:", self.grid.seen_points)
                        print("Way Points:", self.grid.way_points)
                        print("------------------------------------------------")
                        print()
                        print()
                                    
                elif event.type == self.MOUSEBUTTONDOWN and not pathfind_mode:
                    if event.button == 1:     
                        button_down=True                       
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, OBSTACLE)
                        if cells:
                            for obstacle_cell in cells:
                                self.draw_cell(obstacle_cell)

                    if event.button == 2:
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, EMPTY)
                        if cells:
                            for remove_cell in cells:
                                self.draw_cell(remove_cell)

                    if event.button == 3:
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, STARTING_POINT)
                        if cells:
                            for starting_cell in cells:
                                self.draw_cell(starting_cell)
                
                elif event.type == self.MOUSEBUTTONUP and not pathfind_mode:
                    button_down=False

                if event.type == self.MOUSEMOTION and button_down==True and not pathfind_mode:
                    cells = self.grid.find_and_change_type_of_cell(pos_mouse, OBSTACLE)
                    if cells:
                        for obstacle_cell in cells:
                            self.draw_cell(obstacle_cell)
                                        
            #sets time of the page updating             
            self.clock.tick(100)

            #shows the progress on screen
            pygame.display.flip()

        #when the main loop is interrupted the programm quits
        pygame.quit()
        
        
if __name__ == "__main__":
    print("This is the drawing board module")