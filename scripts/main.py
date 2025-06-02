import random
import pygame
from pygame.locals import *
from game import TronGame
from LightTrail import LightTrail


pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("TRON")

#inicialización del juego
tron_game = TronGame()



tron_game.player1.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
tron_game.player2.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda




while tron_game.running:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            tron_game.running = False
        
        if event.type == pygame.KEYDOWN:
            # Player 1
            if event.key == tron_game.mapping_player1['left']:
                tron_game.player1.change_direction(pygame.Vector2(-1, 0))
            elif event.key == tron_game.mapping_player1['right']:
                tron_game.player1.change_direction(pygame.Vector2(1, 0))
            elif event.key == tron_game.mapping_player1['up']:
                tron_game.player1.change_direction(pygame.Vector2(0, -1))
            elif event.key == tron_game.mapping_player1['down']:
                tron_game.player1.change_direction(pygame.Vector2(0, 1))

            if event.key == tron_game.mapping_player1['toggle']:  #Cuando queira apagar/encender la estela de luz, este botón tendrá un 70% de probabilidad de funcionar
                if random.random() < 0.7:
                    tron_game.player1.trailEnabled = not tron_game.player1.trailEnabled
                    
                    print("trial toggled p1")
                else:
                    print("trial toggle p1 failed")
            

            # Player 2
            if event.key == tron_game.mapping_player2['left']:
                tron_game.player2.change_direction(pygame.Vector2(-1, 0))
            elif event.key == tron_game.mapping_player2['right']:
                tron_game.player2.change_direction(pygame.Vector2(1, 0))
            elif event.key == tron_game.mapping_player2['up']:
                tron_game.player2.change_direction(pygame.Vector2(0, -1))
            elif event.key == tron_game.mapping_player2['down']:
                tron_game.player2.change_direction(pygame.Vector2(0, 1))

            if event.key == tron_game.mapping_player2['toggle']:  #Cuando queira apagar/encender la estela de luz, este botón tendrá un 70% de probabilidad de funcionar
                if random.random() < 0.7:
                    tron_game.player2.trailEnabled = not tron_game.player2.trailEnabled
                    
                    print("trial toggled p2")
                else:
                    print("trial toggle p2 failed")

    tron_game.screen.fill((0, 0, 0))  # <--- limpia la pantalla

    tron_game.player1.draw_player()
    tron_game.player2.draw_player()
    
    tron_game.update_state()
    pygame.display.flip()

pygame.quit()