import pygame
from player import Player
from LightTrail import LightTrail
import numpy as np
import random

class TronGame:
    def __init__(self, render=True):

        self.render = render
        self.simulated_time = 0

        #diccionario de teclas para cada jugador
        self.mapping_player1 = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s,
            'toggle': pygame.K_LSHIFT 

        }

        self.mapping_player3 = {
            'left': pygame.K_f,
            'right': pygame.K_h,
            'up': pygame.K_t,
            'down': pygame.K_g,
            'toggle': pygame.K_RALT
        }

        self.mapping_player2 = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'toggle': pygame.K_RSHIFT
        }

        self.mapping_player4 = {
            'left': pygame.K_j,
            'right': pygame.K_l,
            'up': pygame.K_i,
            'down': pygame.K_k,
            'toggle': pygame.K_RCTRL
        }

        

        self.mapping_player4 = {
            'left': pygame.K_j,
            'right': pygame.K_l,
            'up': pygame.K_i,
            'down': pygame.K_k,
            'toggle': pygame.K_RCTRL
        }

        width = 1400
        height = 840

        if self.render:
            self.screen = pygame.display.set_mode((width, height))
        else: 
            self.screen = None    
        self.cell_size = 40 #la casilla es de 40x40 pixeles, es decir, hay 35 casillas en horizontal y 20 en vertical
        self.grid_cols = width // self.cell_size  #cambiado a columnas
        self.grid_rows = height // self.cell_size #cambiado a filas

        self.borders = []
        for col in range(self.grid_cols):
            self.borders.append((col,0))        #borde superior
            self.borders.append((col, self.grid_rows-1))  #borde inferior
        for row in range(self.grid_rows-1):
            self.borders.append((0,row+1))
            self.borders.append((self.grid_cols-1, row+1))

        ######generación de mapas
        self.borders = set(self.borders)  #convertir a set 

        self.other_maps = random.randint(1, 4) #elige un mapa al azar entre 1 y 4
        if self.other_maps == 1:
            self.borders.update((col, 5) for col in range(5, 14)) 
            self.borders.update((col, 15) for col in range(21, 30))
            self.borders.update((17, row) for row in range(4, 17))


        if self.other_maps == 2:
            self.borders.update((col, row) for col in range(3, 13) for row in (4, 12))
            self.borders.update((col, row) for col in range(22, 32) for row in (8, 16))
            self.borders.update((22, row) for row in range(4, 8))
            self.borders.update((12, row) for row in range(13, 17))
            self.borders.update((17, row) for row in range(8, 13))


        if self.other_maps == 3:
            self.borders.update((col, 16) for col in range(3,10))
            self.borders.update((col, 10) for col in range(9,27))
            self.borders.update((col, 4) for col in range (25,32))
            self.borders.update((17, row) for row in range (4,7))
            self.borders.update((17, row) for row in range (14,17))
            
        if self.other_maps == 4:

            self.borders.update((col, row) for col in range (9,14) for row in (6,14))
            self.borders.update((col, row) for col in range (21,26) for row in (6,14))
            self.borders.update((col, row) for row in range(4, 6) for col in (11,17))
            self.borders.update((col, row) for row in range(15, 17) for col in (17, 23))
            self.borders.update([(17,6),(17,7),(17,13),(17,14),(13,10),(21,10)])

        
########Inicializar jugadores
        self.player1 = Player(3, 6, self.screen, "RED", self.cell_size, self.mapping_player1, team="RED")
        self.player2 = Player(31, 6, self.screen, "BLUE", self.cell_size, self.mapping_player2, team="BLUE")
        self.player3 = Player(3, 14, self.screen, "RED", self.cell_size, self.mapping_player3, team="RED")
        self.player4 = Player(31, 14, self.screen, "BLUE", self.cell_size, self.mapping_player4, team="BLUE")



        self.trail1 = LightTrail(self.player1, "RED")
        self.trail2 = LightTrail(self.player2, "BLUE")
        self.trail3 = LightTrail(self.player3, "RED")
        self.trail4 = LightTrail(self.player4, "BLUE")

        self.player1.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
        self.player2.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda
        self.player3.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
        self.player4.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda



        self.clock = pygame.time.Clock()
        self.running = True

        self.players = [self.player1, self.player2, self.player3, self.player4]  #lista de jugadores
        self.trails = [self.trail1, self.trail2, self.trail3, self.trail4] # lista de trazos de luz
       


    def check_collitions(self):
        for i, player in enumerate(self.players):
            if not player.isAlive:  #Si el jugador esta muerto no compara sus colisiones
                continue

            player_pos = (int(player.position.x), int(player.position.y))       #recorre los jugadores y guarda sus posiciones

            if not player.has_moved:        #si el jugador ya se movio detecta colisiones (evitar colision en el frame inicial)
                continue

            for trail in self.trails:   #recorre las listas de trazos de luz
                if player_pos in trail.lightCords:    #si las posiciones coinciden hay colision
                    
                    """"#Aqui se identifica quien murio y con que estela
                    if trail.player == player:      #muerte por estela propia
                            print(f"Jugador {i+1} ({player.color}) colisionó con **su propia** estela en: {player_pos[0]},{player_pos[1]}")
                    else:   #muerte por estela enemiga
                        print(f"Jugador {i+1} ({player.color}) colisionó con la estela **enemiga** en: {player_pos[0]},{player_pos[1]}")
                    """
                    
                    player.isAlive = False 
                    break  # Detenemos después de la primera colisión
            
            for (x,y) in self.borders:
                if (x,y) == player_pos:
                    #print(f"El jugador {i+1} colisiono con un muro")   #Colisiona con un muro
                    player.isAlive = False
                    break
        
    def draw_borders(self):
        for (x, y) in self.borders:
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            if self.render:
                pygame.draw.rect(self.screen, (200,200,200), rect)
    
    def update_state(self, dt):

        self.simulated_time += dt/1000.0

        for trail in self.trails:
            trail.updateTrail(self.simulated_time)

        # Actualizamos el movimiento de cada jugador con su propias teclas
        for player in self.players:
            player.move(dt)
        
        self.check_collitions() #comprueba colisiones
        
    
    def draw(self):
        if not self.render:
            return
        self.screen.fill((0,0,0))
        self.draw_borders()

        for trail in self.trails:
            trail.drawTrail(self.screen, self.cell_size, self.simulated_time)
        for player in self.players:
            player.draw_player()


        
   


