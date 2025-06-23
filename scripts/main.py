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
                    
                    print("trial toggled p3")
                else:
                    print("trial toggle p3 failed")
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
                    
                    print("trial toggled p4")   
                else:
                    print("trial toggle p4 failed")
            

        

    tron_game.screen.fill((0, 0, 0))  # <--- limpia la pantalla

    for player in player_list:
        player.draw_player()

    tron_game.check_collitions()

    if not tron_game.player1.isAlive and not tron_game.player2.isAlive and not tron_game.player3.isAlive and not tron_game.player4.isAlive:
            tron_game.running = False


    

    tron_game.update_state()
    
    tron_game.build_Obs_Matrix() #construye la matriz de observación

    obstacles = tron_game.get_obstacles_from_obs() #matriz de obtaculos extraida de la matriz del tensor de observación

    #player 1
    vision1 = tron_game.player1.get_cone_vision(tron_game.grid_cols, tron_game.grid_rows, obstacles) #retorna un set de coordenadas (x,y) que son visibles para el jugador 1
    obs_visible1 = tron_game.get_obs_in_vision(tron_game.obs, vision1) #retorna un tensor con las observaciones de las casillas visibles en el cono de visión

    #player 2
    vision2 = tron_game.player2.get_cone_vision(tron_game.grid_cols, tron_game.grid_rows, obstacles) #retorna un set de coordenadas (x,y) que son visibles para el jugador 2
    obs_visible2 = tron_game.get_obs_in_vision(tron_game.obs, vision2) #retorna un tensor con las observaciones de las casillas visibles en el cono de visión

    #player 3
    vision3 = tron_game.player3.get_cone_vision(tron_game.grid_cols, tron_game.grid_rows, obstacles) #retorna un set de coordenadas (x,y) que son visibles para el jugador 3
    obs_visible3 = tron_game.get_obs_in_vision(tron_game.obs, vision3) #retorna un tensor con las observaciones de las casillas visibles en el cono de visión

    #player 4 
    vision4 = tron_game.player4.get_cone_vision(tron_game.grid_cols, tron_game.grid_rows, obstacles) #retorna un set de coordenadas (x,y) que son visibles para el jugador 4
    obs_visible4 = tron_game.get_obs_in_vision(tron_game.obs, vision4) #retorna un tensor con las observaciones de las casillas visibles en el cono de visión

    

    for (x, y) in vision1: #dibuja el cono de visión del jugador 1
        s = pygame.Surface((tron_game.cell_size, tron_game.cell_size), pygame.SRCALPHA)
        s.fill((255, 255, 0, 80))  # Amarillo semitransparente
        tron_game.screen.blit(s, (x * tron_game.cell_size, y * tron_game.cell_size))

    for (x, y) in vision2: #dibuja el cono de visión del jugador 2
        s = pygame.Surface((tron_game.cell_size, tron_game.cell_size), pygame.SRCALPHA)
        s.fill((0, 255, 255, 80))  # Cyan semitransparente
        tron_game.screen.blit(s, (x * tron_game.cell_size, y * tron_game.cell_size))
    
    for (x, y) in vision3: #dibuja el cono de visión del jugador 3
        s = pygame.Surface((tron_game.cell_size, tron_game.cell_size), pygame.SRCALPHA)
        s.fill((255, 0, 255, 80))  # Magenta semitransparente
        tron_game.screen.blit(s, (x * tron_game.cell_size, y * tron_game.cell_size))    

    for (x, y) in vision4: #dibuja el cono de visión del jugador 4
        s = pygame.Surface((tron_game.cell_size, tron_game.cell_size), pygame.SRCALPHA)
        s.fill((255, 165, 0, 80))  # Naranja        
        tron_game.screen.blit(s, (x * tron_game.cell_size, y * tron_game.cell_size))
        
    
    #print(np.linspace(2, 19, 4))


    pygame.display.flip()

pygame.quit()