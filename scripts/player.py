import pygame
from pygame.math import Vector2

class Player:
    def __init__(self, x, y, screen, color):
        self.position = Vector2(x, y)
        self.speed = 12  # Velocidad de movimiento
        self.screen = screen
        self.color = color

    def move(self, keys):

        print("entra a actualziar estado player")

        direction = Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            direction.x = -1
        if keys[pygame.K_RIGHT]:
            direction.x = 1
        if keys[pygame.K_UP]:
            direction.y = -1
        if keys[pygame.K_DOWN]:
            direction.y = 1
        if keys[pygame.K_a]:
            direction.x = -1
        if keys[pygame.K_d]:
            direction.x = 1
        if keys[pygame.K_w]:
            direction.y = -1
        if keys[pygame.K_s]:
            direction.y = 1

        if direction.length() > 0:
            direction = direction.normalize() * self.speed

        self.position += direction

    def draw_player(self):
        pygame.draw.circle(self.screen, self.color, (int(self.position.x), int(self.position.y)), 23)
