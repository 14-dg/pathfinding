import pygame

from constants import *
from cell import Cell
from grid import Grid
from pathfinder import Pathfinder


class DrawingBoard:
    def __init__(self, grid: Grid, pf: Pathfinder) -> None:
        self.grid = grid
        self.pf = pf
        
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
        
        #shows screen
        self.screen = pygame.display.set_mode(self.grid.get_screen_dimensions())
        
        #makes how fast it updates in ms
        self.clock = pygame.time.Clock()

        #sets title
        pygame.display.set_caption("PATHFINDER")
        
        
        self.colors=[BLACK, WHITE, GREEN, RED, ORANGE, ALICEBLUE, BLUEVIOLET, DEEPSKYBLUE]
        self.pick_color=ALICEBLUE
        
    def draw_cell(self, c: Cell) -> None:
        pygame.draw.rect(self.screen , c.color, (c.x, c.y, c.w, c.h))
    
    def draw_board(self):
        for h in self.grid.grid:
            for c in h:
                self.draw_cell(c)
                
       
    def mainloop(self):
        
        self.draw_board()
        
        button_down = False
        running = True
        
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
                
                #checks key presses
                elif event.type == pygame.KEYDOWN:
                    #checks for return key
                    if event.key == pygame.K_RETURN:
                        self.pf.find()
                    elif event.key == pygame.K_SPACE:                            
                        self.grid.clear_board()
                        self.draw_board()
                    elif event.key == pygame.K_p:
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, TARGET)
                        if cells:
                            # self.pf.add_target(target_cell)
                            for target_cell in cells:
                                self.draw_cell(target_cell)
                                    
                elif event.type == self.MOUSEBUTTONDOWN:
                    if event.button == 1:     
                        button_down=True                       
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, OBSTACLE)
                        if cells:
                            # self.pf.add_obstacle(obstacle_cell)
                            for obstacle_cell in cells:
                                self.draw_cell(obstacle_cell)

                    if event.button == 2:
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, EMPTY)
                        if cells:
                            # self.pf.remove_board_cell(remove_cell)
                            for remove_cell in cells:
                                self.draw_cell(remove_cell)

                    if event.button == 3:
                        cells = self.grid.find_and_change_type_of_cell(pos_mouse, STARTING_POINT)
                        if cells:
                            # self.pf.add_starting_point(starting_cell)
                            for starting_cell in cells:
                                self.draw_cell(starting_cell)
                
                elif event.type == self.MOUSEBUTTONUP:
                    button_down=False

                if event.type == self.MOUSEMOTION and button_down==True:
                    cells = self.grid.find_and_change_type_of_cell(pos_mouse, OBSTACLE)
                    if cells:
                        # self.pf.add_obstacle(obstacle_cell)
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