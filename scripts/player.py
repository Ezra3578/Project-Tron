import pygame

class Player:
    def __init__(self, x, y, screen, color):
        self.x = x
        self.y = y
        self.speed = 12 
        self.screen = screen
        self.color = color

    def move(self, keys):
        # Movimiento horizontal p1
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed 

        # Movimiento vertical p1
        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed

        # Movimiento horizontal p2
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed 

        # Movimiento vertical p2
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed

    def draw_player(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 23)
     