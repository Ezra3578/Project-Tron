import pygame
from pygame.locals import *
from game import TronGame


pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("TRON")
dt = 0

#inicialización del juego
tron_game = TronGame()

tron_game.player1.direction.x = 1
tron_game.player2.direction.x = -1



while tron_game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tron_game.running = False

    tron_game.screen.fill((0, 0, 0))  # <--- limpia la pantalla

    tron_game.player1.draw_player()
    tron_game.player2.draw_player()
    
    tron_game.update_state()
    pygame.display.flip()
    dt = clock.tick(60)

pygame.quit()