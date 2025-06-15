import pygame
from player import Player
from LightTrail import LightTrail
import numpy as np

class TronGame:
    def __init__(self):
        
        #diccionario de teclas para cada jugador
        self.mapping_player1 = {
            'left': pygame.K_a,
            'right': pygame.K_d,
            'up': pygame.K_w,
            'down': pygame.K_s,
            'toggle': pygame.K_LSHIFT 

        }
        self.mapping_player2 = {
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'toggle': pygame.K_RSHIFT
        }

        self.screen = pygame.display.set_mode((1360, 800))
        self.cell_size = 40 #la casilla es de 40x40 pixeles
        self.grid_cols = self.screen.get_width() // self.cell_size  #cambiado a columnas
        self.grid_rows = self.screen.get_height() // self.cell_size #cambiado a filas

        self.borders = []
        for col in range(self.grid_cols):
            self.borders.append((col,0))        #borde superior
            self.borders.append((col, self.grid_rows-1))  #borde inferior
        for row in range(self.grid_rows-1):
            self.borders.append((0,row+1))
            self.borders.append((self.grid_cols-1, row+1))

        self.player1 = Player(2, 9, self.screen, "RED", self.cell_size, self.mapping_player1)
        self.player2 = Player(29, 9, self.screen, "BLUE", self.cell_size, self.mapping_player2)

        self.trail1 = LightTrail(self.player1, "RED")
        self.trail2 = LightTrail(self.player2, "BLUE")

        self.obs = np.zeros((8, self.grid_rows, self.grid_cols), dtype=np.float32) #crea una matriz de ceros con 8 niveles/dimensiones, y con ancho y alto del mapa ((1280, 720))


        self.clock = pygame.time.Clock()
        self.running = True

        self.players = [self.player1, self.player2]
        self.trails = [self.trail1, self.trail2]


    def check_collitions(self):
        for i, player in enumerate(self.players):
            player_pos = (int(player.position.x), int(player.position.y))       #recorre los jugadores y guarda sus posiciones

            if player.has_moved:        #si el jugador ya se movio detecta colisiones (evitar colision en el frame inicial)
            
                for trail in self.trails:   #recorre las listas de trazos de luz
                    for (x, y, _) in trail.lightPoints:
                        if (x, y) == player_pos:    #si las posiciones coinciden hay colision
                                if trail.player == player:      #muerte por estela propia
                                    print(f"Jugador {i+1} ({player.color}) colisionó con **su propia** estela en: {x},{y}")
                                else:   #muerte por estela enemiga
                                    print(f"Jugador {i+1} ({player.color}) colisionó con la estela **enemiga** en: {x},{y}")
                                player.isAlive = False
                                break  # Detenemos después de la primera colisión
                
                for (x,y) in self.borders:
                    if (x,y) == player_pos:
                        print(f"El jugador {i+1} colisiono con un muro")
                        player.isAlive = False
                        break
        
    def draw_borders(self):
        for (x, y) in self.borders:
            rect = pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (200,200,200), rect)
    
    def update_state(self):
        
        self.build_Obs_Matrix()

        dt = self.clock.tick(60)


        for trail in self.trails:
            trail.updateTrail()
            trail.drawTrail(self.screen, self.cell_size)



        # Actualizamos el movimiento de cada jugador con su propias teclas
        for player in self.players:
            player.move(dt)

    def build_Obs_Matrix(self):
        """
        Llena self.obs (shape: 8 x filas x columnas) usando coordenadas de casillas.
        Niveles:
        0: Bordes
        1: Player 1
        2: Player 2
        3: Estelas
        4: Dirección X player 1
        5: Dirección Y player 1
        6: Dirección X player 2
        7: Dirección Y player 2
        """
        self.obs.fill(0)  # limpia todo

        # Nivel 0: Bordes
        for (x, y) in self.borders:
            if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                self.obs[0, y, x] = 1.0

        # Nivel 1: Player 1
        x1, y1 = int(self.player1.position.x), int(self.player1.position.y)
        if 0 <= x1 < self.grid_cols and 0 <= y1 < self.grid_rows:
            self.obs[1, y1, x1] = 1.0

        # Nivel 2: Player 2
        x2, y2 = int(self.player2.position.x), int(self.player2.position.y)
        if 0 <= x2 < self.grid_cols and 0 <= y2 < self.grid_rows:
            self.obs[2, y2, x2] = 1.0

        # Nivel 3: Estelas
        for trail in self.trails:
            for (x, y, _) in trail.lightPoints:
                if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                    self.obs[3, y, x] = 1.0

        # Nivel 4 y 5: Dirección player 1
        if 0 <= x1 < self.grid_cols and 0 <= y1 < self.grid_rows:
            self.obs[4, y1, x1] = self.player1.direction.x
            self.obs[5, y1, x1] = self.player1.direction.y

        # Nivel 6 y 7: Dirección player 2
        if 0 <= x2 < self.grid_cols and 0 <= y2 < self.grid_rows:
            self.obs[6, y2, x2] = self.player2.direction.x
            self.obs[7, y2, x2] = self.player2.direction.y

        
    def get_obstacles_from_obs(self):
        # obs: shape (8, filas, columnas)
        # 0: Bordes, 1: Player 1, 2: Player 2, 3: Estelas
        # 0=libre, 1=muro, 2=estela, 3=jugador
        mat = np.zeros((self.grid_rows, self.grid_cols), dtype=np.int8)
        mat[self.obs[0] == 1] = 1  # Bordes
        mat[self.obs[3] == 1] = 2  # Estelas
        mat[self.obs[1] == 1] = 3  # Player 1
        mat[self.obs[2] == 1] = 3  # Player 2
        return mat

    def get_obs_in_vision(self, obs, vision):  #retornará un tensor con las observaciones de las casillas visibles en el cono de visión
        """
        obs: np.ndarray de shape (8, filas, columnas)
        vision: set de (x, y) coordenadas visibles
        Devuelve: np.ndarray de shape (num_casillas_visibles, 8)
        """
        obs_list = []
        for (x, y) in vision:  #compara cada dato del set de visión con las coordenadas del tensor obs
            obs_list.append(obs[:, y, x]) #extrae la observación de cada casilla visible del tensor obs
        if obs_list:
            return np.stack(obs_list) #devuelve un tensor con las observaciones de las casillas visibles (filas = num_casillas_visibles_cono, columnas = 8)
        else:
            return np.zeros((0, obs.shape[0])) #devuelve un tensor vacío si no hay casillas visibles



