#imports following programms
import pygame, sys, random, time, math
#imports the mixer for the music 
from pygame import mixer
from colorama import Fore, Style,  Back

#import kivy
#from kivy.app import App
#from kivy.uix.label import Label

class pathfinder():
    def __init__(self):        
        
        self.found=False
        self.obstacle = []
        self.goal1 = []
        self.goal2 = []
        self.pos_rect = []
        self.pos_rect2 = []
        self.pos_rect3 = []
        self.pos_rect4 = []        
        self.way = []
        self.way2 = []

    
    def main(self):
        self.next_find = 0  
        self.x_find = 0
        self.y_find = 0
        self.vec_find = 0    
        self.distance = 0        
        self.duration = 0
        self.next_goal = 0
        self.next2 = 0

        #lets pygame initialate and makes it usebale
        pygame.init()

        pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
        myfont = pygame.font.SysFont('Comic Sans MS', 50)

        next_1=0

        #lets the peogramm detect a mouse press
        MOUSEBUTTONUP = pygame.MOUSEBUTTONUP
        MOUSEBUTTONDOWN = pygame.MOUSEBUTTONDOWN
        MOUSEMOTION = pygame.MOUSEMOTION
        mouse = pygame.mouse.get_pressed()

        not_removed = False

        #sets margin
        #margin_x=2
        #margin_y=2
        margin=2

        
        #height_circle = 250
                
        #sets size of screen
        screen_width=1500
        screen_height=750
        size=[screen_width, screen_height]

        #shows screen
        screen = pygame.display.set_mode(size)
        
        #sets diameter of the circle
        height=25
        #width=15               
        
        
        #makes how fast it updates in ms
        clock = pygame.time.Clock()

        #sets title
        pygame.display.set_caption("PATHFINDER")

        #sets colors
        BLACK  = (0, 0, 0)
        WHITE  = (255, 255, 255)
        GREEN  = (0, 255, 0)
        RED    = (255, 0, 0)
        ORANGE = (255, 140, 0)
        ALICEBLUE  = (120, 200, 255)
        BLUEVIOLET = (138, 43, 226)
        DEEPSKYBLUE= (0,191,255)
        #sets which colors are used
        colors=[BLACK, WHITE, GREEN, RED, ORANGE, ALICEBLUE, BLUEVIOLET, DEEPSKYBLUE]
        pick_color=ALICEBLUE

        #lets player click the circles
        button = pygame.display.set_mode(size)
        button = button.get_rect()

        self.distance=margin+height
                                
        def draw_squares(which):
            pos=[]
            f=0
            for column in range(0+margin, screen_height, height+margin):
                for row in range(0+margin, screen_width, height+margin):
                    pos.append(0)
                    pos[f]=([row, column])
                    if which==0:                    
                        pygame.draw.rect(screen , ALICEBLUE, (pos[f][0], pos[f][1], height, height))
                    else:
                        pass
                    f+=1  
            if which == 0:
                return
            elif which == 1:
                return pos
            elif which == 2:
                return f  

        def hit_squares(which_click, pos_click):
            found =False 
            found2=False     
            while not found and not found2:          
                pos=draw_squares(1)
                f1=draw_squares(2)
                                                                            
                #checks for right click
                pos_click2=[pos_click[0], pos_click[1]]   
                    
                #definiert den Bereich der Kreise und fargt ob die Maus in diesem Bereich gecklickt hat
                for f in range(0, f1):
                    pos_x_w_0= pos[f][0]
                    pos_y_w_1= pos[f][1]  

                    pos_click_x2=pos_click2[0]
                    pos_click_y2=pos_click2[1]

                    #print(pos_x_w_0+10)
                    #print(right_click_x)
                    #print(pos_x_w_0-10)
                    #print()
                    #print(pos_x_w_1+10)
                    #print(right_click_y)
                    #print(pos_x_w_1-10)
                    #print()

                    if pos_x_w_0+height > pos_click_x2 > pos_x_w_0 and pos_y_w_1+height > pos_click_y2 > pos_y_w_1:
                        #makes circle where you right clicked threee times as bigger
                        if which_click=="left":
                            pygame.draw.rect(screen , WHITE, (pos[f][0], pos[f][1], height, height))                            
                            self.obstacle.append([pos_x_w_0, pos_y_w_1])

                        elif which_click=="right":
                            pygame.draw.rect(screen , RED, (pos[f][0], pos[f][1], height, height))                              
                            self.goal1.extend([pos_x_w_0, pos_y_w_1])                                   

                        elif which_click=="middle":
                            pygame.draw.rect(screen , ALICEBLUE, (pos[f][0], pos[f][1], height, height)) 
                            self.goal1.remove([pos_x_w_0, pos_y_w_1])
                            self.goal2.remove([pos_x_w_0, pos_y_w_1])
                            self.obstacle.remove([pos_x_w_0, pos_y_w_1])                            

                        elif which_click=="p":
                            pygame.draw.rect(screen , GREEN, (pos[f][0], pos[f][1], height, height))                             
                            self.goal2.extend([pos_x_w_0, pos_y_w_1])
                        found=True
                    else:
                        pass   
                found2=True         

        #red finds green and avoids white
        def find():      
            if self.next_find==0:
                self.pos_rect.append(self.goal1)   
                self.duration=0 
                self.next_find+=1
            else:                    
                if check_if_found() == False:
                    expand()
                    #time.sleep(0.2)
                else:
                    pass
                
                                        
            

        def check_if_found():            
            for i in range(0, len(self.pos_rect)):
                if self.pos_rect[i][0] == self.goal2[0] and self.pos_rect[i][1] == self.goal2[1]:
                    pygame.draw.rect(screen , GREEN, (self.goal2[0], self.goal2[1], height, height))
                    found()
                    return True
                else:
                    pygame.draw.rect(screen , GREEN, (self.goal2[0], self.goal2[1], height, height))
            return False

        def expand():        
            self.pos_rect4 = []
            self.duration+=1    
            for i in self.pos_rect:                
                x=-1
                self.pos_rect3 = []
                #print(self.pos_rect3)
                self.pos_rect2 = []
                self.pos_rect2.append(i)
                self.way.extend([[i, self.duration]])
                #print(Back.RED)
                #print(self.pos_rect)
                #print(self.pos_rect2)
                #print(self.pos_rect3)
                #print(self.pos_rect4)
                #print(Style.RESET_ALL)
                                                  
                                
                #self.pos_rect2.append([self.pos_rect[i][0]+height+margin, self.pos_rect[i][1]+height+margin])                
                #pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect[i][0], self.pos_rect[i][1], height, height))

                #self.pos_rect2.append([self.pos_rect[i][0]+height+margin, self.pos_rect[i][1]-height-margin]) 
                #pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect[i][0], self.pos_rect[i][1], height, height))

                #self.pos_rect2.append([self.pos_rect[i][0]-height-margin, self.pos_rect[i][1]+height+margin])   
                #pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect[i][0], self.pos_rect[i][1], height, height))

                #self.pos_rect2.append([self.pos_rect[i][0]-height-margin, self.pos_rect[i][1]-height-margin])
                #pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect[i][0], self.pos_rect[i][1], height, height))
                
                    
                if if_go(1)==True:                    
                    self.pos_rect3.append([self.pos_rect2[0][0]+self.distance, self.pos_rect2[0][1]]) 
                    x+=1               
                    pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect3[x][0], self.pos_rect3[x][1], height, height))
                    #time.sleep(0.5)
                
                if if_go(2)==True:                    
                    self.pos_rect3.append([self.pos_rect2[0][0], self.pos_rect2[0][1]-self.distance]) 
                    x+=1
                    pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect3[x][0], self.pos_rect3[x][1], height, height))
                    #time.sleep(0.5)

                if if_go(3)==True:                    
                    self.pos_rect3.append([self.pos_rect2[0][0]-self.distance, self.pos_rect2[0][1]])   
                    x+=1
                    pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect3[x][0], self.pos_rect3[x][1], height, height))
                    #time.sleep(0.5)

                if if_go(4)==True:                    
                    self.pos_rect3.append([self.pos_rect2[0][0], self.pos_rect2[0][1]+self.distance])
                    x+=1
                    pygame.draw.rect(screen , BLUEVIOLET, (self.pos_rect3[x][0], self.pos_rect3[x][1], height, height))
                    #time.sleep(0.5)

            #for x in self.pos_rect3:
                #pygame.draw.rect(screen , BLUEVIOLET, (x, height, height))
        

                self.pos_rect4.extend(self.pos_rect3)
                
                
                #print(Back.GREEN)
                #print(self.pos_rect)
                #print(self.pos_rect2)
                #print(self.pos_rect3)
                #print(self.pos_rect4)
                #print(Style.RESET_ALL)

            self.way = get_relavent_pos("way", 0)
                       
            get_new_pos()
            #print(self.pos_rect)
            get_relavent_pos("rect", 0)
            #print(self.pos_rect)
                        
            #print(self.pos_rect)
            #print(self.pos_rect2)

        def get_relavent_pos(which, x):  
            if which== "rect":
                i=0
                x=0
                for target in self.pos_rect:
                    i+=1
                    x=0
                    for goal in self.pos_rect:
                        x+=1
                        if target == goal and x != i:
                            #print("here")
                            self.pos_rect.pop(x-1)
                return self.pos_rect

            elif which=="way":
                i=0
                x=0
                for target in self.way:
                    i+=1
                    x=0
                    for goal in self.way:
                        x+=1
                        if target[0] == goal[0] and x != i:
                            #print("here")
                            #print(self.way)
                            self.way.pop(x-1)
                return self.way

            elif which=="way2":
                i=0
                x=0
                for target in self.way2:
                    i+=1
                    x=0
                    for goal in self.way2:
                        x+=1
                        if target[0] == goal[0] and x != i:
                            #print("here")
                            #print(self.way)
                            self.way2.pop(x-1)
                return self.way2

            elif which=="next_goal":  
                time.sleep(1)
                next_goal1=0    
                next_goal2=0  
                next_goal3=0  
                next_goal4=0            
                for target in self.next_goal:
                                        
                    if [[x[0][0]-self.distance, x[0][1]], x[1]] == target    :
                        next_goal1 = 1
                    
                    elif [[x[0][0], x[0][1]-self.distance], x[1]] == target:   
                        next_goal2 = 1
                        
                    elif [[x[0][0]+self.distance, x[0][1]], x[1]] == target:
                        next_goal3 = 1

                    elif [[x[0][0], x[0][1]+self.distance], x[1]] == target:
                        next_goal4 = 1

                if next_goal1 == 1:
                    self.next_goal.append([[x[0][0]-self.distance, x[0][1]], x[1]])

                elif next_goal2 == 0:
                    self.next_goal.append([[x[0][0], x[0][1]-self.distance], x[1]])

                elif next_goal3 == 0:
                    self.next_goal.append([[x[0][0]+self.distance, x[0][1]], x[1]])

                elif next_goal4 == 0:
                    self.next_goal.append([[x[0][0], x[0][1]+self.distance], x[1]])
                        
        
        #def get_all_pos():
            #self.pos_rect.extend(self.pos_rect4)
                        
        def get_new_pos():     
            self.pos_rect=[] 
            #print(self.pos_rect)      
            self.pos_rect.extend(self.pos_rect4)
            
        def obstacle():
            x=[]
            for b in self.obstacle:
                #print(b)
                if [self.pos_rect2[0][0]+self.distance, self.pos_rect2[0][1]] == b:  
                    x.append(1) 

                if [self.pos_rect2[0][0], self.pos_rect2[0][1]-self.distance] == b:                               
                    x.append(2)
                
                if [self.pos_rect2[0][0]-self.distance, self.pos_rect2[0][1]] == b:                               
                    x.append(3)
                
                if [self.pos_rect2[0][0], self.pos_rect2[0][1]+self.distance] == b:                            
                    x.append(4)                
            return x

        def if_go(which):
            if self.obstacle != []:
                x=[]
                x.extend(obstacle())
                for c in x: 
                    if c == which:
                        return False
                return True
            else:
                return True

        
        def found():
            print("found")  
            #print(self.duration)
            self.found=True
            self.way.extend([[self.goal2, self.duration]])
            self.way2.extend([[self.goal2, self.duration]])
            #print(len(self.way))   
            #print(self.way) 
            clean_way()
            #print(len(self.way))   
            #print(self.way2)
            for i in range(0, len(self.way2)):  
                if i !=1 and i != 2: 
                    #print(i)
                    #print(self.way2)
                    pygame.draw.rect(screen , ORANGE, (self.way2[i][0][0], self.way2[i][0][1], height, height))
                else:
                    pass
            pygame.draw.rect(screen , GREEN, (self.goal2[0], self.goal2[1], height, height))


                        
                  
            #for i in self.way_2:
                #pygame.draw.rect(screen , BLUEVIOLET, (i[0], i[1], height, height))

        def clean_way():

            self.next_goal=[]
            self.next2 = -1

            #for i in range(1, self.duration, -1):
            for x in self.way:
                if x[1]==self.duration and x[0] != self.goal2:
                    pass
                    #print(x)
                    #print(self.goal2)
                    #self.way.remove(x)
                elif x[1]==self.duration and x[0] == self.goal2:
                    #get_relavent_pos("next_goal", x)
                    self.way2.extend(x)
                    #self.next2+=1
                    #print(len(self.next_goal))
                    
            
            #print(self.duration)
            #print(sorted(self.way))
            
            if neighboors([self.goal2, self.duration])==False:
                print("yas")
                return

            
            
        def neighboors(x):
            

            a=b=c=d=[1]

            if x[0] == self.goal1:
                return False

            for i in self.way:                
                
                if [[x[0][0]-self.distance, x[0][1]], x[1]] == i:
                    print(1, i, x)
                    self.way2.append(i)
                    #time.sleep(1)
                    call_neighboors([[x[0][0]-self.distance, x[0][1]], x[1]-1])
                    #a.pop(0)
                    #a.extend(i)
                
                elif [[x[0][0], x[0][1]-self.distance], x[1]] == i:   
                    print(2, i, x)
                    self.way2.append(i)
                    #time.sleep(1)
                    call_neighboors([[x[0][0], x[0][1]-self.distance], x[1]-1] )
                    #b.pop(0)
                    #b.extend(i)
                    
                elif [[x[0][0]+self.distance, x[0][1]], x[1]] == i:
                    print(3, i, x)
                    self.way2.append(i)
                    #time.sleep(1)
                    call_neighboors([[x[0][0]+self.distance, x[0][1]], x[1]-1])
                    #c.pop(0)
                    #c.extend(i)

                elif [[x[0][0], x[0][1]+self.distance], x[1]] == i:
                    print(4, i, x)
                    self.way2.append(i)
                    #time.sleep(1)
                    call_neighboors([[x[0][0], x[0][1]+self.distance], x[1]-1])
                    #d.pop(0)
                    #d.extend(i)
                       


        def call_neighboors(x):
            neighboors(x)        

        def last_clean():
            randomizer = random.randint(1, 1)
            get_relavent_pos("way2", 0)  
            for i in range(self.duration):
                for x in self.way2:
                    pass
            
                
                

        #def delete_except_neighboors(which):
            #which.pop(0)
            #print(len(self.way))
            #reset()
            #for x in self.way:
                #if x[1]==which[1] and x[0] != which[0]:
                    #print(x)
                    #print(self.goal2)
                    #self.way.remove(x)
                #elif x[1]==self.duration and x[0] == which[0]:
                    #get_relavent_pos("next_goal", x)
                    #self.next2+=1
                    #print(len(self.next_goal))

                #pygame.draw.rect(screen , RED, (x[0][0], x[0][1], height, height))
            #print(len(self.way))
            
        def reset():
            screen.fill(BLACK)
            draw_squares(0) 
            self.next_find = 0  
            self.x_find = 0
            self.y_find = 0
            self.vec_find = 0    
            self.distance = 0        
            self.duration = 0
            self.next_goal = 0
            self.next2 = 0
            self.found=False
            self.obstacle = []
            self.goal1 = []
            self.goal2 = []
            self.pos_rect = []
            self.pos_rect2 = []
            self.pos_rect3 = []
            self.pos_rect4 = []        
            self.way = []
            self.way2 = []
              
       

        def main():
        
            #sets when to exit
            done=False

            button_down=False

            reset()

            #main loop
            while not done:                 
                
                #This creates a new object on which you can call the render method.
                textsurface = myfont.render("HELLO", False, RED)
                
                screen.blit(textsurface,(650,0))

                # --- Main event loop
                #checks every event
                for event in pygame.event.get():
                    #gets position of the mouse
                    pos_mouse = pygame.mouse.get_pos()
                    #checks if you close the page
                    if event.type == pygame.QUIT:
                        #quits main loop
                        done = True
                    
                    #checks key presses
                    elif event.type == pygame.KEYDOWN:
                        #checks for return key
                        if event.key == pygame.K_RETURN:
                            find()
                        elif event.key == pygame.K_SPACE:                            
                            reset()
                        elif event.key == pygame.K_p:
                            click = pos_mouse
                            hit_squares("p", click)
                                        
                    elif event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:     
                            button_down=True                       
                            left_click = pos_mouse
                            hit_squares("left", left_click)

                        if event.button == 2:
                            middle_click = pos_mouse
                            hit_squares("middle", middle_click)

                        if event.button == 3:
                            right_click = pos_mouse
                            hit_squares("right", right_click)
                    
                    elif event.type == MOUSEBUTTONUP:
                        button_down=False

                    if event.type == MOUSEMOTION and button_down==True:
                        left_click = pos_mouse
                        hit_squares("left", left_click)
                        
                #sets time of the page updating             
                clock.tick(100000)

                #shows the progress on screen
                pygame.display.flip()

            #when the main loop is interrupted the programm quits
            pygame.quit()
            sys.exit()

        main()
        


#print(Style.RESET_ALL)
p1 = pathfinder()
p1.main()
