import pygame
from player import Player
class TronGame:
    def __init__(self):
        screen = pygame.display.set_mode((1280, 720))

        self.player1 = Player(128, 360, screen, "RED")
        self.player2 = Player(1152, 360, screen, "BLUE")

        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        #diccionario de teclas para cada jugador
        self.mapping_player1 = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s

        }
        self.mapping_player2 = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN
        }

    
    
    def update_state(self):
        
        pygame.event.pump()
        key = pygame.key.get_pressed()
        
        # Actualizamos el movimiento de cada jugador con su propias teclas
        self.player1.move(key, self.mapping_player1)
        self.player2.move(key, self.mapping_player2)

            

        


