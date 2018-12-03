# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 13:22:13 2018

@author: Daniel
"""

import pygame
import random

#from statistics import median, mean
#from collections import Counter

LR = .6
discount = .6

pygame.init()    
pygame.display.set_caption('snake')
clock = pygame.time.Clock() 

white = (255,255,255)
black = (0,0,0)
white = (255,255,255)
red = (255, 0, 0)
display_width = 500
display_height = 500
gameDisplay = pygame.display.set_mode((display_width, display_height))

"""
Q table works by comapring the action with the possible reward, 4 actions 
nothing minus 1, get a cherry plus 100, hit a will minus 100, hit yourself minus 100

initilalizes like this
      |  WALL | CHERRY | SELF | NOT |
UP        0       0     0      0
-----   
LEFT      0       0     0      0
-----
DOWN      0       0     0      0
-----
RIGHT     0       0     0      0

comparisons using 2 numbers, relative position of cherry to head, and length of body
example

{Length, [X, Y] { UP, DOWN, LEFT, RIGHT }}
{  3   , [1, 2] {  0,   0,   0,   0     }}


Q leanign formula is as follows

Q(s(probability), a(action)) = OLD_Q_VALUE + at[learning rate] * (reward + discount * estimization of optimal future value - OLD VALUE)

so in our snakes case lets take left for example with nothing in the 2 squares in front 
[] [] snake

learning rate .5

discount .9

Q(s, left) = 0 + .5 * (-1 + .9 * -1 - 0)
Q(s, left) = -.95

again for cherry two in fron left
cherry [] snake

Q(s, left) = -.95 + .4(-1 + .9 * 100 - -.95)
Q(s, left) = 70.01
"""

Qmatrix = [[(random.randrange(-100, 100)/10) for i in range(4)]] * 4

cherry_score = 9
wall_score = -10
self_score = -9
nothing = 2



def Predict(Direction, Python, cherry):
    score = []
    Distance_to_left_wall = Python.body[0][0]
    Distance_to_right_wall = display_width - Python.body[0][0] 
    Distance_to_top = Python.body[0][1]
    Distance_to_bottom = display_height - Python.body[0][1]
    
    
        
    #up
    if Direction == 0:
        
        if cherry.y < Python.body[0][1]:
            score.append(cherry_score)
            
        if Distance_to_left_wall <= 4 :
            score.append(wall_score)
            
        if Distance_to_right_wall <= 4:
            score.append(wall_score)
            
        if Distance_to_top <= 4 :
            score.append(wall_score)
            
        
        
                
        
       
    #left
    if Direction == 1:
        
        if cherry.x < Python.body[0][0]:
            score.append(cherry_score)
            
        if Distance_to_left_wall <= 4 :
            score.append(wall_score)
            
        if Distance_to_bottom <= 4:
            score.append(wall_score)
            
        if Distance_to_top <= 4 :
            score.append(wall_score)
            
            
                
        
                
        
            
    #down
    if Direction == 2:
        
        if cherry.y > Python.body[0][1]:
            score.append(cherry_score)
            
        if Distance_to_bottom >= 4 :
            score.append(wall_score)
            
                
       
                
        
            
    #right
    if Direction == 3:
        
        if cherry.x > Python.body[0][0]:
            score.append(cherry_score)
            
        if Distance_to_right_wall <= 4 :
            score.append(wall_score)
            
        if Distance_to_bottom <= 4:
            score.append(wall_score)
            
        if Distance_to_top <= 4 :
            score.append(wall_score)
            
                
       
    if len(score) < 1:
        score.append(nothing)
     
    
    return max(score)
        
        
def Q_Update(Python, cherry):
    
    Distance_to_left_wall = Python.body[0][0]
    Distance_to_right_wall = display_width - Python.body[0][0] 
    Distance_to_ceiling = Python.body[0][1]
    Distance_to_bottom = display_height - Python.body[0][1]
    Distance_to_cherry = [cherry.x - Python.body[0][0], cherry.y - Python.body[0][1]]
    
    this_value = 0
    future_value = 0
    
    projected_list = []
    
    event = 0
    
    for Direction in range(4):
        #up
        if Direction == 0:
            if Distance_to_ceiling <= 4:
                this_value = wall_score
                event = 0
            elif Distance_to_cherry[1] < -2:
                this_value = cherry_score
                event = 1
            elif (overlap(Python.body[0][0], Python.body[0][1] - 4, Python.size, 20, i.body[0][0], i.body[0][1]) for i in Python.body[1:]):
                this_value = self_score
                event = 2
            else:
                this_value = nothing
                event = 3
                
                
            future_value = Predict(Direction, Python, cherry)
                
            newQ = Qmatrix[Direction][event] + LR * (this_value + discount * future_value - Qmatrix[Direction][event])
            
            Qmatrix[Direction][event] = newQ
            
            projected_list.append(newQ)
        
        #left movement
        if Direction == 1:
            if Distance_to_left_wall <= 4:
                this_value = wall_score
                event = 0
            elif Distance_to_cherry[0] < -2:
                this_value = cherry_score
                event = 1
            elif (overlap(Python.body[0][0] - 4, Python.body[0][1], Python.size, 20, i.body[0][0], i.body[0][1]) for i in Python.body[1:]):
                this_value = self_score
                event = 2
            else:
                this_value = -1
                event = 3
                
            future_value = Predict(Direction, Python, cherry)
                
            newQ = Qmatrix[Direction][event] + LR * (this_value + discount * future_value - Qmatrix[Direction][event])
            
            Qmatrix[Direction][event] = newQ
            
            projected_list.append(newQ)
                
        #down
        if Direction == 2:
            if Distance_to_bottom <= 6:
                this_value = wall_score
                event = 0
            elif Distance_to_cherry[1] < 2:
                this_value = cherry_score
                event = 1
            elif (overlap(Python.body[0][0], Python.body[0][1] + 4, Python.size, 20, i.body[0][0], i.body[0][1]) for i in Python.body[1:]):
                this_value = self_score
                event = 2
            else:
                this_value = nothing
                event = 3
                
            
                
            future_value = Predict(Direction, Python, cherry)
                
            newQ = Qmatrix[Direction][event] + LR * (this_value + discount * future_value - Qmatrix[Direction][event])
            
            Qmatrix[Direction][event] = newQ
            
            projected_list.append(newQ)
                
            
        
        
        #right
        if Direction == 3:
            if Distance_to_right_wall <= 4:
                this_value = wall_score
                event = 0
            elif Distance_to_cherry[0] < 2:
                this_value = cherry_score
                event = 1
            if (overlap(Python.body[0][0] - 4, Python.body[0][1], Python.size, 20, i.body[0][0], i.body[0][1]) for i in Python.body[1:]):
                this_value = self_score
                event = 2
            else:
                this_value = nothing
                event = 3
                
            
            future_value = Predict(Direction, Python, cherry)
                
            newQ = Qmatrix[Direction][event] + LR * (this_value + discount * future_value - Qmatrix[Direction][event])
            
            Qmatrix[Direction][event] = newQ
            
            projected_list.append(newQ)
            
    return projected_list
                
    
            
        
        
        
        
    

def text_objects( text, font):
    
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text, size, location):
    
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = location
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    
def overlap(selfx, selfy, selfSize, size, X, Y):
    
    if ((selfx > X + 2 and selfx < X + size - 2 or selfx+selfSize > X and selfx + selfSize < X + size) and ((selfy > Y + 2 and selfy < Y + size - 2 or selfy+selfSize > Y and selfy + selfSize < Y + size))):
        return True
    else:
        return False
    
    
    

def game_loop():
    
    
    move_list = []
    
    for x in range(20):
        Python = snake()
        cherry = pointCherry()
        print("Run %d" % (x))
        running = True
        last = pygame.time.get_ticks()
        previous = 0
        highest = 5
        
        while running:
            #this is the handeling loop, that handles all keyboard output
            now = pygame.time.get_ticks()
            
            
            
            if now - last >= 60:
                
                move_list = Q_Update(Python, cherry)
                if previous == 0:
                    move_list[2] = -100
                elif previous == 1:
                    move_list[3] = -100
                elif previous == 2:
                    move_list[0] = -100
                else:
                    move_list[1] = -100
                print(move_list)
                highest = move_list.index(max(move_list))
                last = now
                previous = highest
                print(highest)
                
                if highest == 0:
                        Python.moveUp()

                elif highest == 1:
                        Python.moveLeft()

                elif highest == 2:
                        Python.moveDown()

                elif highest == 3:
                        Python.moveRight()
                    
     
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    
              
            
            
            
            
            #basically blank the screen refresh it
            gameDisplay.fill(black)  
            
            #draw everything 
            cherry.draw()  
            Python.draw()
            message_display(format("Score: %d" % (Python.length - 3)), 20, (40, 15) )
            
            #change the direction of the "Snake"
            Python.main_loop() 
            
            
            #once again call the overlap function to see if the snake and cherry overlap every frame
            if overlap(cherry.x, cherry.y, cherry.size, Python.size, Python.body[0][0], Python.body[0][1]):
                Python.score += 1
                Python.update()
                cherry.update()
            
            #check to see if the head touches the border 
            if (Python.body[0][0] > display_width - Python.size or Python.body[0][0] < 0 or Python.body[0][1] > display_height - Python.size or Python.body[0][1] < 0):
                running = False
                
            #check to see if the head is inside the body at any point
            for x, i in enumerate(Python.body):
                if x > 3:
                    if overlap(Python.body[0][0], Python.body[0][1], Python.size, Python.size, i[0], i[1]):
                        running = False
                     
#            original collision checking, only saw if the entire head overlapped the body            
            if (Python.body[0] in Python.body[1:-1]):
                running = False
            
            #I have an extra if statement because the crash happens before the update, so sometimes
            #it tries to update even though the game ended
            
            
            
            if running:
                pygame.display.update()
            
                
            clock.tick(60)

        
                
    
    
        
       
        
class snake(object):
    
    def __init__(self):
        self.length = 3
        self.last = pygame.time.get_ticks()
        self.size = 20
        self.step = 2
        self.score = 0
        self.body = [[display_width/2 - x * 10, display_height/2] for x in range(self.length)]
        self.direction = 0
        
    def update(self):
        self.body.append([self.body[-1][0], self.body[-1][1]])
        self.length += 1
        
    def main_loop(self):
        now = pygame.time.get_ticks()
        if (now - self.last) >= 160:
            self.last = now
            for i in range(self.length-1,0,-1):
                self.body[i] = self.body[i - 1]
        if self.direction == 0:
            self.body[0] = [self.body[0][0] + self.step, self.body[0][1]]
        if self.direction == 1:
            self.body[0] = [self.body[0][0] - self.step, self.body[0][1]]
        if self.direction == 2:
            self.body[0] = [self.body[0][0] , self.body[0][1] - self.step]
        if self.direction == 3:
            self.body[0] = [self.body[0][0], self.body[0][1] + self.step]
            
    def moveRight(self):
        self.direction = 0
        
    def moveLeft(self):
        self.direction = 1
        
    def moveUp(self):
        self.direction = 2
        
    def moveDown(self):
        self.direction = 3 
        
    def draw(self):
        for i in range(len(self.body)):
            pygame.draw.rect(gameDisplay, white, ((self.body[i][0],self.body[i][1]),(self.size,self.size)))
        
    
    def getScore(self):
        return self.score
    
class pointCherry():
    
    def __init__(self):
        self.size = 15
        self.x = random.randint(20, display_width - self.size)
        self.y = random.randint(20, display_height - self.size)
        self.rect = pygame.rect.Rect((self.x, self.y),(self.size, self.size))
        
    def update(self):
        self.x = random.randint(20, display_width - self.size)
        self.y = random.randint(20, display_height - self.size)
        
    def draw(self):
        self.rect = pygame.rect.Rect((self.x, self.y),(self.size, self.size))
        pygame.draw.rect(gameDisplay, red, self.rect)
        
        

game_loop()
#print(loop)
#training_data_save = np.array(training_data)
#    np.save('saved.npy',training_data_save)
pygame.quit()

print(Qmatrix)






