import pygame
class Player:
    def __init__(self, x, y, direction, screen, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.trail = [(x,y)]
        self.screen = screen
        self.color = color
    
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
    
    def draw_player(self):
        pygame.draw.circle(self.screen, self.color,(self.x,self.y), 23)


            