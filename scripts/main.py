import pygame
from pygame.locals import *
from game import TronGame

pygame.init()
clock = pygame.time.Clock()
running = True
pygame.display.set_caption("TRON")
dt = 0

#inicialización del juego
tron_game = TronGame()


while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    tron_game.player1.draw_player()
    tron_game.player2.draw_player()

    

    tron_game.update_state()
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(60)

pygame.quit()