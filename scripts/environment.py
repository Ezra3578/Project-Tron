from pettingzoo.utils import ParallelEnv
from gymnasium import spaces
from game import TronGame

import pygame
import numpy as np

def pad_observation(obs_visible, max_length=30): # Asegura que la observación tenga una longitud fija y llena de ceros si es necesario
    current_len = obs_visible.shape[0] # Número de casillas visibles en el cono de visión
    # Si la longitud actual es menor que la máxima, rellenamos con ceros
    if current_len < max_length:
        padding = np.zeros((max_length - current_len, obs_visible.shape[1]), dtype=np.float32)
        return np.vstack((obs_visible, padding))
    elif current_len > max_length: # Si la longitud actual es mayor que la máxima, recortamos
        return obs_visible[:max_length]  # Recortamos si se pasa
    return obs_visible

class TronParallelEnv(ParallelEnv):
    def __init__(self):
        super().__init__()
        self.game = TronGame(render=True)  # Inicializa el juego Tron renderizando
        self.screen = self.game.screen
        self.agents = ['player_1', 'player_2', 'player_3', 'player_4']

        self.players_dict = {
            
            'player_1': self.game.player1,
            'player_2': self.game.player2,
            'player_3': self.game.player3,
            'player_4': self.game.player4,
        }

        self.possible_agents = self.agents.copy()
        self.obs = np.zeros((14, self.game.grid_rows, self.game.grid_cols), dtype=np.float32)  # Matriz de observación (14 niveles, filas, columnas)
        self.observation_space = {
            agent: spaces.Box(low=0, high=1, shape=(30, 14), dtype=np.float32)  # 30 casillas visibles máximo (coordenadas del cono de visión), 14 canales
            for agent in self.agents
        }
        self.action_space = {
            agent: spaces.Discrete(4)  # 4 direcciones 
            for agent in self.agents
        }
    
    def reset(self):
        pass
    def step(self, actions):
        pass

  

   
    def observe(self, agent): #agent debe ser self.game.player1, player2, player3 o player4

        player = self.players_dict[agent]
        obstacles = self.get_obstacles_from_obs()  # Obtiene la matriz de obstáculos del juego principal

        if player.isAlive:
            vision = player.get_cone_vision(self.game.grid_cols, self.game.grid_rows, obstacles) # obtiene las coordenadas visibles en el cono de visión del jugador
            obs_visible = self.get_obs_in_vision(self.obs, vision) #extrae las observaciones de las casillas visibles del cono de visión (combina las coordenadas visibles con la matriz de obstáculos)
        else:
            vision = set()
            obs_visible = np.zeros((0, self.obs.shape[0]), dtype=np.float32) 
        
    
        
        obs_padded = pad_observation(obs_visible)
        assert obs_padded.shape == self.observation_space[agent].shape, "Observe no coincide con observation_space"
        return obs_padded, vision # Devuelve la observación del jugador con padding si es necesario, son observaciones tipo np.ndarray de forma (30, 14) y los conos de cada jugador
            
    

    def get_obstacles_from_obs(self):  # extrae los obstaculos de la matriz de observación para cada frame
        # obs: shape (14, filas, columnas)
        # 0: Bordes, 1: Player 1, 2: Player 2, 3: Player 3, 4: Player 4, 5: Estelas
        # 0=libre, 1=muro, 2=estela, 3=jugador
        mat = np.zeros((self.game.grid_rows, self.game.grid_cols), dtype=np.int8) #genera una matriz de ceros con el tamaño del mapa (filas, columnas)
        # Asignar valores a la matriz de obstáculos
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
            obs_list.append(obs[:, y, x]) #extrae la observación de cada casilla visible del tensor obs (combina vocion del cono y obtaculos)
        if obs_list:
            return np.stack(obs_list) #devuelve un tensor con las observaciones de las casillas visibles (filas = num_casillas_visibles_cono, columnas = 14 canales)
        else:
            return np.zeros((0, obs.shape[0])) #devuelve un tensor vacío si no hay casillas visibles


    def draw_visions(self, visions):
        # Colores de visión por jugador
        vision_colors = [(255, 255, 0, 80), (0, 255, 255, 80), (255, 0, 255, 80), (255, 165, 0, 80)]

        for i, agent in enumerate(self.agents):
            player = self.players_dict[agent]
            vision = visions[i]  # Se asume que `visions` tiene siempre 4 elementos, aunque estén vacíos

            if not player.isAlive:
                continue

            for x, y in vision:
                s = pygame.Surface((self.game.cell_size, self.game.cell_size), pygame.SRCALPHA)
                s.fill(vision_colors[i])
                self.screen.blit(s, (x * self.game.cell_size, y * self.game.cell_size))




    def update_state(self, dt):
        self.game.update_state((dt))
        self.build_Obs_Matrix()


    @property
    def player1(self):
        return self.game.player1

    @property
    def player2(self):
        return self.game.player2

    @property
    def player3(self):
        return self.game.player3

    @property
    def player4(self):
        return self.game.player4

    @property
    def mapping_player1(self):
        return self.game.mapping_player1

    @property
    def mapping_player2(self):
        return self.game.mapping_player2

    @property
    def mapping_player3(self):
        return self.game.mapping_player3

    @property
    def mapping_player4(self):
        return self.game.mapping_player4

    @property
    def render(self):
        return self.game.render

    @property
    def running(self):
        return self.game.running
    

    def draw(self):
        return self.game.draw()
    
    @property
    def clock(self):
        return self.game.clock

 
    @running.setter
    def running(self, value):
        self.game.running = value

    

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
            for (x, y) in self.game.borders:
                if 0 <= x < self.game.grid_cols and 0 <= y < self.game.grid_rows:
                    self.obs[0, y, x] = 1.0

            # Nivel 1: Player 1
            x1, y1 = int(self.player1.position.x), int(self.player1.position.y)
            if 0 <= x1 < self.game.grid_cols and 0 <= y1 < self.game.grid_rows:
                self.obs[1, y1, x1] = 1.0

            # Nivel 2: Player 2
            x2, y2 = int(self.player2.position.x), int(self.player2.position.y)
            if 0 <= x2 < self.game.grid_cols and 0 <= y2 < self.game.grid_rows:
                self.obs[2, y2, x2] = 1.0
            
            # Nivel 3: Player 3
            x3, y3 = int(self.player3.position.x), int(self.player3.position.y)
            if 0 <= x3 < self.game.grid_cols and 0 <= y3 < self.game.grid_rows:
                self.obs[3, y3, x3] = 1.0

            # Nivel 4: Player 4
            x4, y4 = int(self.player4.position.x), int(self.player4.position.y)
            if 0 <= x4 < self.game.grid_cols and 0 <= y4 < self.game.grid_rows:
                self.obs[4, y4, x4] = 1.0

            # Nivel 5: Estelas
            for trail in self.game.trails:
                for (x, y, _) in trail.lightPoints:
                    if 0 <= x < self.game.grid_cols and 0 <= y < self.game.grid_rows:
                        self.obs[5, y, x] = 1.0

            # Nivel 6 y 7: Dirección player 1
            if 0 <= x1 < self.game.grid_cols and 0 <= y1 < self.game.grid_rows:
                self.obs[6, y1, x1] = self.player1.direction.x
                self.obs[7, y1, x1] = self.player1.direction.y

            # Nivel 8 y 9: Dirección player 2
            if 0 <= x2 < self.game.grid_cols and 0 <= y2 < self.game.grid_rows:
                self.obs[8, y2, x2] = self.player2.direction.x
                self.obs[9, y2, x2] = self.player2.direction.y

            # Nivel 10 y 11: Dirección player 3
            if 0 <= x3 < self.game.grid_cols and 0 <= y3 < self.game.grid_rows:
                self.obs[10, y3, x3] = self.player3.direction.x
                self.obs[11, y3, x3] = self.player3.direction.y

            # Nivel 12 y 13: Dirección player 4
            if 0 <= x4 < self.game.grid_cols and 0 <= y4 < self.game.grid_rows:
                self.obs[12, y4, x4] = self.player4.direction.x
                self.obs[13, y4, x4] = self.player4.direction.y