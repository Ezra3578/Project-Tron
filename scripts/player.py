import pygame
class Player:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.trail = [(x,y)]
        
    
    def move(self):
        if self.direction == "UP":
            self.y += 1
        elif self.direction == "RIGHT":
            self.x += 1
        elif self.direction == "LEFT":
            self.x -=1
        elif self.direction == "DOWN":
            self.y -=1
    
    def set_direction(self, direction):
        self.direction = direction
    

            