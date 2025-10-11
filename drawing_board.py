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
        
        self.margin = 2
        self.length_squares = 25
        
        #sets size of screen
        self.screen_width=1500
        self.screen_height=750
        self.size=[self.screen_width, self.screen_height]
        
        #shows screen
        self.screen = pygame.display.set_mode(self.size)
        
        #makes how fast it updates in ms
        self.clock = pygame.time.Clock()

        #sets title
        pygame.display.set_caption("PATHFINDER")
        
        
        self.colors=[BLACK, WHITE, GREEN, RED, ORANGE, ALICEBLUE, BLUEVIOLET, DEEPSKYBLUE]
        self.pick_color=ALICEBLUE
        
    
    
    def draw_board(self):
        for column in range(0+self.margin, self.screen_height, self.length_squares+self.margin):
            for row in range(0+self.margin, self.screen_width, self.length_squares+self.margin):
                pygame.draw.rect(self.screen , ALICEBLUE, (row, column, self.length_squares, self.length_squares))

        
    def get_cell_from_mouse_pos(self, pos_mouse: tuple) -> Cell:
        return Cell()
    
    def add_starting_point(self, cell):
        pass
    
    def add_target(self, cell):
        pass
    
    def add_obstacle(self, cell):
        pass
    
    def remove_board_cell(self, cell):
        pass
        
    
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
                        pass
                    elif event.key == pygame.K_p:
                        click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        self.add_target(click_cell)
                        self.pf.add_target(click_cell)
                                    
                elif event.type == self.MOUSEBUTTONDOWN:
                    if event.button == 1:     
                        button_down=True                       
                        left_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        self.add_obstacle(left_click_cell)
                        self.pf.add_obstacle(left_click_cell)

                    if event.button == 2:
                        middle_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        self.remove_board_cell(middle_click_cell)
                        self.pf.remove_board_cell(middle_click_cell)

                    if event.button == 3:
                        right_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        self.add_starting_point(right_click_cell)
                        self.pf.add_starting_point(right_click_cell)
                
                elif event.type == self.MOUSEBUTTONUP:
                    button_down=False

                if event.type == self.MOUSEMOTION and button_down==True:
                    left_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                    self.pf.add_obstacle(left_click_cell)
                    
            #sets time of the page updating             
            self.clock.tick(100)

            #shows the progress on screen
            pygame.display.flip()

        #when the main loop is interrupted the programm quits
        pygame.quit()
        
        
if __name__ == "__main__":
    db = DrawingBoard(Grid(), Pathfinder(Grid()))
    db.mainloop()