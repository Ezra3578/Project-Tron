import pygame
from pygame.math import Vector2

class Player:
    def __init__(self, x, y, screen, color, cell_size, key_mapping):
        self.position = Vector2(x, y) #posición en cada frame
        self.old_position = Vector2(x,y) #posicion anterior
        self.direction = Vector2(0, 0) #vector dirección al que apunta

        self.screen = screen
        self.color = color

        self.trailEnabled = True

        self.cell_size = cell_size
        self.size = self.cell_size // 2
        
        self.move_delay = 150 #ms entre movimientos
        self.time_since_move = 0 #cuenta el tiempo desde que se mueve

        self.key_mapping = key_mapping


    def getTrailEstate(self):
        return self.trailEnabled
    

    def move(self, dt):

        self.time_since_move += dt

        if self.time_since_move >= self.move_delay:
            self.time_since_move = 0
            self.old_position = self.position.copy() #se guarda la posicion antes de moverse para luego pasarla al trazo de luz
            self.position += self.direction    #actualiza la posición
        

    def change_direction(self, new_dir):
        # Cambia de dirección si no es la contraria
        if new_dir.x != -self.direction.x and new_dir.y != -self.direction.y:
            self.direction = new_dir

    def draw_player(self):
        #drawing now by squares and not pixels. Although, to calculate where is it drawn it must be focused on pixels 
        pixel_x = int(self.position.x * self.cell_size + self.cell_size // 2) #puts the center of the player on the center of the map square
        pixel_y = int(self.position.y * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(self.screen, self.color, (pixel_x, pixel_y), self.size - 2)

