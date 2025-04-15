import pygame
from pygame.locals import *
from game import TronGame
from LightTrail import LightTrail

pygame.init()
clock = pygame.time.Clock()
#running = True
pygame.display.set_caption("TRON")
dt = 0

#inicialización del juego
tron_game = TronGame()

tron_game.player1.direction.x = 1
tron_game.player2.direction.x = -1

trail1 = LightTrail(tron_game.player1, "RED")
trail2 = LightTrail(tron_game.player2, "BLUE")

while tron_game.running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tron_game.running = False

    tron_game.screen.fill((0, 0, 0))  # <--- limpia la pantalla

    trail1.updateTrail()
    trail2.updateTrail()

    trail1.drawTrail(tron_game.screen)
    trail2.drawTrail(tron_game.screen)

    

    tron_game.player1.draw_player()
    tron_game.player2.draw_player()
    
    tron_game.update_state()
    pygame.display.flip()
    dt = clock.tick(60)

pygame.quit()