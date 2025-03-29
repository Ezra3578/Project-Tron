import pygame
from player import Player
class TronGame:
    def __init__(self):

        self.player1 = Player(128, 360, "RIGHT")
        self.player2 = Player(1152, 360, "LEFT")

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
    
    def update_with_key(self, key):

        key = pygame.key.get_pressed()

        if key[pygame.K_w]:
            self.player1.set_direction("UP")

        if key[pygame.K_a]:
            self.player1.set_direction("LEFT")

        if key[pygame.K_s]:
            self.player1.set_direction("DOWN")

        if key[pygame.K_d]:
            self.player1.set_direction("RIGHT")

        if key[pygame.K_UP]:
            self.player2.set_direction("UP")

        if key[pygame.K_DOWN]:
            self.player2.set_direction("DOWN")

