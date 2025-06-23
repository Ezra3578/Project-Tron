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

        

        self.screen = pygame.display.set_mode((1360, 800))
        self.cell_size = 40 #la casilla es de 40x40 pixeles, es decir, hay 34 casillas en horizontal y 20 en vertical

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


        self.player1 = Player(2, 7, self.screen, "RED", self.cell_size, self.mapping_player1, team="RED") 
        self.player2 = Player(31, 7, self.screen, "BLUE", self.cell_size, self.mapping_player2, team="BLUE")
        self.player3 = Player(2, 13, self.screen, "RED", self.cell_size, self.mapping_player3, team="RED")
        self.player4 = Player(31, 13, self.screen, "BLUE", self.cell_size, self.mapping_player4, team="BLUE")

        self.player1 = Player(2, 9, self.screen, "RED", self.cell_size, self.mapping_player1)
        self.player2 = Player(29, 9, self.screen, "BLUE", self.cell_size, self.mapping_player2)


        self.trail1 = LightTrail(self.player1, "RED")
        self.trail2 = LightTrail(self.player2, "BLUE")
        self.trail3 = LightTrail(self.player3, "RED")
        self.trail4 = LightTrail(self.player4, "BLUE")

        self.obs = np.zeros((14, self.grid_rows, self.grid_cols), dtype=np.float32) #crea una matriz de ceros con 14 niveles/dimensiones, y con ancho y alto del mapa (self.grid_cols, self.grid_rows)


        self.clock = pygame.time.Clock()
        self.running = True


        self.players = [self.player1, self.player2, self.player3, self.player4]  #lista de jugadores
        self.trails = [self.trail1, self.trail2, self.trail3, self.trail4] # lista de trazos de luz
       

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
        3: Player 3
        4: Player 4
        5: Estelas
        6: Dirección X player 1
        7: Dirección Y player 1
        8: Dirección X player 2
        9: Dirección Y player 2
        10: Dirección X player 3
        11: Dirección Y player 3
        12: Dirección X player 4
        13: Dirección Y player 4
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
        
        # Nivel 3: Player 3
        x3, y3 = int(self.player3.position.x), int(self.player3.position.y)
        if 0 <= x3 < self.grid_cols and 0 <= y3 < self.grid_rows:
            self.obs[3, y3, x3] = 1.0

        # Nivel 4: Player 4
        x4, y4 = int(self.player4.position.x), int(self.player4.position.y)
        if 0 <= x4 < self.grid_cols and 0 <= y4 < self.grid_rows:
            self.obs[4, y4, x4] = 1.0

        # Nivel 5: Estelas
        for trail in self.trails:
            for (x, y, _) in trail.lightPoints:
                if 0 <= x < self.grid_cols and 0 <= y < self.grid_rows:
                    self.obs[5, y, x] = 1.0

        # Nivel 6 y 7: Dirección player 1
        if 0 <= x1 < self.grid_cols and 0 <= y1 < self.grid_rows:
            self.obs[6, y1, x1] = self.player1.direction.x
            self.obs[7, y1, x1] = self.player1.direction.y

        # Nivel 8 y 9: Dirección player 2
        if 0 <= x2 < self.grid_cols and 0 <= y2 < self.grid_rows:
            self.obs[8, y2, x2] = self.player2.direction.x
            self.obs[9, y2, x2] = self.player2.direction.y

        # Nivel 10 y 11: Dirección player 3
        if 0 <= x3 < self.grid_cols and 0 <= y3 < self.grid_rows:
            self.obs[10, y3, x3] = self.player3.direction.x
            self.obs[11, y3, x3] = self.player3.direction.y

        # Nivel 12 y 13: Dirección player 4
        if 0 <= x4 < self.grid_cols and 0 <= y4 < self.grid_rows:
            self.obs[12, y4, x4] = self.player4.direction.x
            self.obs[13, y4, x4] = self.player4.direction.y

    def get_obstacles_from_obs(self):
        # obs: shape (14, filas, columnas)
        # 0: Bordes, 1: Player 1, 2: Player 2, 3: Player 3, 4: Player 4, 5: Estelas
        # 0=libre, 1=muro, 2=estela, 3=jugador
        mat = np.zeros((self.grid_rows, self.grid_cols), dtype=np.int8)
        mat[self.obs[0] == 1] = 1  # Bordes
        mat[self.obs[5] == 1] = 2  # Estelas
        mat[self.obs[1] == 1] = 3  # Player 1
        mat[self.obs[2] == 1] = 3  # Player 2
        mat[self.obs[3] == 1] = 3  # Player 3
        mat[self.obs[4] == 1] = 3  # Player 4
        return mat

    def get_obs_in_vision(self, obs, vision):  #retornará un tensor con las observaciones de las casillas visibles en el cono de visión
        """
        obs: np.ndarray de shape (14, filas, columnas)
        vision: set de (x, y) coordenadas visibles
        Devuelve: np.ndarray de shape (num_casillas_visibles, 14)
        """
        obs_list = []
        for (x, y) in vision:  #compara cada dato del set de visión con las coordenadas del tensor obs
            obs_list.append(obs[:, y, x]) #extrae la observación de cada casilla visible del tensor obs
        if obs_list:
            return np.stack(obs_list) #devuelve un tensor con las observaciones de las casillas visibles (filas = num_casillas_visibles_cono, columnas = 14)
        else:
            return np.zeros((0, obs.shape[0])) #devuelve un tensor vacío si no hay casillas visibles





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




