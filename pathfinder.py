
import pygame
import sys, os
import math


#sets colors
BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
GREEN  = (0, 255, 0)
RED    = (255, 0, 0)
ORANGE = (255, 140, 0)
ALICEBLUE  = (120, 200, 255)
BLUEVIOLET = (138, 43, 226)
DEEPSKYBLUE= (0,191,255)


class drawing_board:
    def __init__(self) -> None:
        #lets pygame initialate and makes it usebale
        pygame.init()

        pygame.font.init() # you have to call this at the start, 
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
        # pos = []
        # f=0
        
        for column in range(0+self.margin, self.screen_height, self.length_squares+self.margin):
            for row in range(0+self.margin, self.screen_width, self.length_squares+self.margin):
                #pos.append(0)
                #pos[f]=([row, column])
                pygame.draw.rect(self.screen , ALICEBLUE, (row, column, self.length_squares, self.length_squares))
                #f+=1

        
    def get_cell_from_mouse_pos(self):
        pass
    
    
    
    def mainloop(self):
        
        self.draw_board()
        
        pathfinder = Pathfinder()
        
        button_down = False
        running = True
        
        #main loop
        while running:                 
            
            #This creates a new object on which you can call the render method.
            textsurface = self.myfont.render("HELLO", False, RED)
            
            self.screen.blit(textsurface,(650,0))

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
                        pathfinder.find()
                    elif event.key == pygame.K_SPACE:                            
                        pass
                    elif event.key == pygame.K_p:
                        click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        pathfinder.add_target(click_cell)
                                    
                elif event.type == self.MOUSEBUTTONDOWN:
                    if event.button == 1:     
                        button_down=True                       
                        left_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        pathfinder.add_obstacle(left_click_cell)

                    if event.button == 2:
                        middle_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        pathfinder.remove_board_cell(middle_click_cell)

                    if event.button == 3:
                        right_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                        pathfinder.add_starting_point(right_click_cell)
                
                elif event.type == self.MOUSEBUTTONUP:
                    button_down=False

                if event.type == self.MOUSEMOTION and button_down==True:
                    left_click_cell = self.get_cell_from_mouse_pos(pos_mouse)
                    pathfinder.add_obstacle(left_click_cell)
                    
            #sets time of the page updating             
            self.clock.tick(100)

            #shows the progress on screen
            pygame.display.flip()

        #when the main loop is interrupted the programm quits
        pygame.quit()



class Pathfinder:
    def __init__(self) -> None:
        pass
    
    def add_target(self):
        pass
    
    def add_starting_point(self):
        pass
    
    def add_obstacle(self):
        pass
    
    def remove_board_cell(self):
        pass
    
    def change_color_of_board_cell(self):
        pass
    

    def find(self):
        pass


def run_simulation():
    animation = drawing_board()
    animation.mainloop()

if __name__ == "__main__":
    run_simulation()