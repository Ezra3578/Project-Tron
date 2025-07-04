import random
import pygame
from pygame.locals import *
from game import TronGame
from LightTrail import LightTrail
import numpy as np


pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption("TRON")

#inicialización del juego
tron_game = TronGame()



tron_game.player1.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
tron_game.player2.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda
tron_game.player3.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
tron_game.player4.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda

player_list = [tron_game.player1, tron_game.player2, tron_game.player3, tron_game.player4] 



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
                    

            # Player 3
            if event.key == tron_game.mapping_player3['left']:
                tron_game.player3.change_direction(pygame.Vector2(-1, 0))
            elif event.key == tron_game.mapping_player3['right']:
                tron_game.player3.change_direction(pygame.Vector2(1, 0))
            elif event.key == tron_game.mapping_player3['up']:
                tron_game.player3.change_direction(pygame.Vector2(0, -1))
            elif event.key == tron_game.mapping_player3['down']:
                tron_game.player3.change_direction(pygame.Vector2(0, 1))
            if event.key == tron_game.mapping_player3['toggle']:  #Cuando queira apagar/encender la estela de luz, este botón tendrá un 70% de probabilidad de funcionar
                if random.random() < 0.7:
                    tron_game.player3.trailEnabled = not tron_game.player3.trailEnabled
                    

            # Player 4
            if event.key == tron_game.mapping_player4['left']:
                tron_game.player4.change_direction(pygame.Vector2(-1, 0))
            elif event.key == tron_game.mapping_player4['right']:
                tron_game.player4.change_direction(pygame.Vector2(1, 0))
            elif event.key == tron_game.mapping_player4['up']:
                tron_game.player4.change_direction(pygame.Vector2(0, -1))
            elif event.key == tron_game.mapping_player4['down']:
                tron_game.player4.change_direction(pygame.Vector2(0, 1))
            if event.key == tron_game.mapping_player4['toggle']:  #Cuando queira apagar/encender la estela de luz, este botón tendrá un 70% de probabilidad de funcionar
                if random.random() < 0.7:
                    tron_game.player4.trailEnabled = not tron_game.player4.trailEnabled
                    
        

    if not tron_game.player1.isAlive and not tron_game.player2.isAlive and not tron_game.player3.isAlive and not tron_game.player4.isAlive:
            tron_game.running = False

    
    tron_game.build_Obs_Matrix() #construye la matriz de observación

    obstacles = tron_game.get_obstacles_from_obs() #matriz de obtaculos extraida de la matriz del tensor de observación

    #Crea listas de las visiones y los objetos visibles
    visions = []
    obs_visible_list = []
    for i, player in enumerate(tron_game.players):
        if player.isAlive:
            vision = player.get_cone_vision(tron_game.grid_cols, tron_game.grid_rows, obstacles)
            obs_visible = tron_game.get_obs_in_vision(tron_game.obs, vision)
        else:
            vision = set()
            obs_visible = np.zeros((0, tron_game.obs.shape[0]), dtype=np.float32)
        visions.append(vision)
        obs_visible_list.append(obs_visible)
    
    if tron_game.render: # Si el renderizado está activado, se limita la velocidad de fotogramas
        dt = tron_game.clock.tick(60)
    else: # Si el renderizado está desactivado, se usa un valor fijo para dt
        dt = 100
        
    tron_game.update_state(dt)  #Aqui se realizan los movimientos, comprueban colisiones y se actualizan los trazos de luz
    tron_game.draw(visions)     #Aqui se dibujan trazos de luz, muros y jugadores

    pygame.display.flip()

pygame.quit()