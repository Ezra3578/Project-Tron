import pygame
from pygame.math import Vector2

class Player:
    def __init__(self, x, y, screen, color):
        self.position = Vector2(x, y) #posición en cada frame
        self.speed = 12  # Velocidad de movimiento
        self.screen = screen
        self.color = color
        self.direction = Vector2(0, 0) #vector dirección al que apunta

    def move(self, keys, key_mapping):
        # key_mapping va a ser un diccionario con las teclas para cada dirección:
        new_direction = Vector2(0, 0) #para realizar el cambio de dirección una vez se cambie la tecla
        
        if keys[key_mapping['left']]:
            new_direction.x = -1
        if keys[key_mapping['right']]:
            new_direction.x = 1
        if keys[key_mapping['up']]:
            new_direction.y = -1
        if keys[key_mapping['down']]:
            new_direction.y = 1

        if new_direction.length() > 0:
            self.direction = new_direction.normalize()

        self.position += self.direction * self.speed    #actualiza la posición

    def draw_player(self):
        pygame.draw.circle(self.screen, self.color, (int(self.position.x), int(self.position.y)), 23)
