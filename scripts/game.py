import pygame
from player import Player
class TronGame:
    def __init__(self):
        screen = pygame.display.set_mode((1280, 720))

        self.player1 = Player(128, 360, screen, "RED")
        self.player2 = Player(1152, 360, screen, "BLUE")

        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
    
    
    def update_state(self):

        key = pygame.key.get_pressed()
    
        if key[pygame.K_w] or key[pygame.K_a] or key[pygame.K_s] or key[pygame.K_d]:
            self.player1.move(key)

        if key[pygame.K_UP] or key[ pygame.K_LEFT] or key[pygame.K_DOWN] or key[ pygame.K_RIGHT]:
            self.player2.move(key)

            

        


