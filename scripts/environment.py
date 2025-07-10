import gymnasium as gym

from pettingzoo.utils.env import ParallelEnv
from game import TronGame

from gymnasium import spaces
from gymnasium.spaces import Discrete

import pygame
import numpy as np
import random

from player import Player
from LightTrail import LightTrail

#Se encarga de tomar la vision del agente y poner fijo el tamaño de la vision (pone 0 en lo que no ve)
def pad_observation(obs_visible, max_length=38): # Asegura que la observación tenga una longitud fija y llena de ceros si es necesario
    current_len = obs_visible.shape[0] # Número de casillas visibles en el cono de visión
    # Si la longitud actual es menor que la máxima, rellenamos con ceros
    if current_len < max_length:
        padding = np.zeros((max_length - current_len, obs_visible.shape[1]), dtype=np.float32)
        return np.vstack((obs_visible, padding))
    elif current_len > max_length: # Si la longitud actual es mayor que la máxima, recortamos
        return obs_visible[:max_length]  # Recortamos si se pasa
    return obs_visible


class TronParallelEnv(ParallelEnv):
    
    metadata = {"render_mode":["human"], "name": "tron"}

    def __init__(self, render_mode=None):
        self.game = None
        self.agents = ['player_1', 'player_2', 'player_3', 'player_4']
        self.possible_agents = self.agents.copy()
        self.visions = []
        self.step_count = 0
        self.max_steps = 600
        self.observation_space = {
            agent: spaces.Box(low=-1, high=1, shape=(38, 14), dtype=np.float32)
            for agent in self.agents
        }
        self.action_space = {
            agent: spaces.Discrete(5)
            for agent in self.agents
        }
        self.render_mode = render_mode
        self.dt = 0
        self.screen = None
        self.observation_spaces = self.observation_space
        self.action_spaces = self.action_space



    def reset(self, *, seed=None, options=None):
        
        self.game = TronGame()    

        self.step_count = 0

        self.obs = np.zeros((14, self.game.grid_rows, self.game.grid_cols), dtype=np.float32)

        if self.render_mode == "human":
            self.game.setScreen(pygame.display.set_mode((self.game.width, self.game.height)))
        else:
            self.game.setScreen(None)

        self.visions = []

        self.player1 = Player(3, 6, self.game.screen, "RED", self.game.cell_size, self.game.mapping_player1, team="RED")
        self.player2 = Player(31, 6, self.game.screen, "BLUE", self.game.cell_size, self.game.mapping_player2, team="BLUE")
        self.player3 = Player(3, 14, self.game.screen, "RED", self.game.cell_size, self.game.mapping_player3, team="RED")
        self.player4 = Player(31, 14, self.game.screen, "BLUE", self.game.cell_size, self.game.mapping_player4, team="BLUE")


        self.trail1 = LightTrail(self.player1, "RED")
        self.trail2 = LightTrail(self.player2, "BLUE")
        self.trail3 = LightTrail(self.player3, "RED")
        self.trail4 = LightTrail(self.player4, "BLUE")

        self.player1.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
        self.player2.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda
        self.player3.direction = pygame.Vector2(1,0) #inicia moviendose a la derecha
        self.player4.direction = pygame.Vector2(-1,0) #inicia moviendose a la izquierda

        self.players_dict = {
            'player_1': self.player1,
            'player_2': self.player2,
            'player_3': self.player3,
            'player_4': self.player4,
        }

        #para las hitbox y dibujar xD
        self.game.players = [self.player1, self.player2, self.player3, self.player4]  #lista de jugadores
        self.game.trails = [self.trail1, self.trail2, self.trail3, self.trail4] # lista de trazos de luz

        self.build_Obs_Matrix()

        observations = {
            agent: self.observe(agent)
            for agent in self.agents
        }

        infos = {agent: {} for agent in self.agents}
    
        return observations, infos


    def step(self, actions):

        #Toma de acciones
        for agent, action in actions.items():
            self.apply_action(agent, action)

        if self.render_mode == "human":
            self.dt = self.game.clock.tick(60)
        else:
            self.dt = 100
        
        # Actualiza el juego
        self.game.update_state(self.dt)

        #Graficar o no
        self.render_screen()

        #Contar el paso
        self.step_count += 1

        #Comprobaciones para finalizacion
        done_by_steps = self.step_count >= self.max_steps
        red_dead = self.team_dead("RED")
        blue_dead = self.team_dead("BLUE")

        #Actualizar datos del mapa
        self.build_Obs_Matrix()

        self.visions = []

        #Se construyen las observaciones
        observations = {
            agent: self.observe(agent)
            for agent in self.agents
        }


        #inicializar recompensas en 0
        rewards = {agent: 0.0 for agent in self.agents}

        # Penalización por paso 
        for agent in self.agents:
            if self.players_dict[agent].isAlive:
                rewards[agent] += -0.1

        #Recompensas y penalizaciones por muertes
        for agent in self.agents:
            player = self.players_dict[agent]

            if not player.isAlive:
                rewards[agent] += -20  # Penalización por morir

                killer = self.find_killer(agent)

                if killer and killer != agent:
                    killer_player = self.players_dict[killer]
                    victim_player = self.players_dict[agent]

                    if killer_player.team != victim_player.team:
                        rewards[killer] += 100  # Recompensar al killer si es enemigo
                    else:
                        # Penalizar por matar a un aliado:
                        rewards[killer] -= 35

        #Recompensas por victorias (sin empate)
        if red_dead != blue_dead and not done_by_steps:
            winning_team = "BLUE" if red_dead else "RED"
            for agent, player in self.players_dict.items():
                if player.team == winning_team:
                    rewards[agent] += 200

                    
        # Termina si el jugador muere
        terminations = {
            agent: not self.players_dict[agent].isAlive
            for agent in self.agents
        }

        terminations["__all__"] = all(terminations.values())

        #Si se cumplen las condiciones se acaba el juego
        if done_by_steps or red_dead or blue_dead:
            truncations = {agent: True for agent in self.agents}
        else:
            truncations = {agent: False for agent in self.agents}
        truncations["__all__"] = any(truncations.values())

        #La info que retornara es si el agente esta vivo, si fue asesinado por quien, el equipo y cuantos pasos lleva
        infos = {}
        for agent in self.agents:
            infos[agent] = {
                "is_alive": self.players_dict[agent].isAlive,
                "killer": self.find_killer(agent),
                "team": self.players_dict[agent].team,
                "step": self.step_count,
            }

        # Filtrar agentes que no deben continuar
        active_agents = [
            agent for agent in self.agents
            if not terminations[agent] and not truncations[agent]
        ]

        # Filtrar observaciones y demás para evitar mezclar trayectorias
        observations = {agent: obs for agent, obs in observations.items() if agent in active_agents}
        rewards = {agent: rewards[agent] for agent in active_agents}
        terminations = {agent: terminations[agent] for agent in active_agents}
        truncations = {agent: truncations[agent] for agent in active_agents}
        infos = {agent: infos[agent] for agent in active_agents}

        # Agrega el campo "__all__" de nuevo después de filtrar
        terminations["__all__"] = len(active_agents) == 0
        truncations["__all__"] = done_by_steps or red_dead or blue_dead

        return observations, rewards, terminations, truncations, infos
    


    def render_screen(self):
        if self.render_mode == "human":
            self.game.render = True
            self.game.draw()
            self.draw_visions(self.visions)
            pygame.display.flip()


   
    def observe(self, agent): #agent debe ser self.game.player1, player2, player3 o player4

        player = self.players_dict[agent]
        obstacles = self.get_obstacles_from_obs()  # Obtiene la matriz de obstáculos del juego principal

        if player.isAlive:
            vision = player.get_cone_vision(self.game.grid_cols, self.game.grid_rows, obstacles) # obtiene las coordenadas visibles en el cono de visión del jugador
            obs_visible = self.get_obs_in_vision(self.obs, vision) #extrae las observaciones de las casillas visibles del cono de visión (combina las coordenadas visibles con la matriz de obstáculos)
        else:
            vision = set()
            obs_visible = np.zeros((0, self.obs.shape[0]), dtype=np.float32) 
        
        self.visions.append(vision)
        
        obs_padded = pad_observation(obs_visible)

        assert obs_padded.shape == self.observation_space[agent].shape, "Observe no coincide con observation_space"
        return obs_padded # Devuelve la observación del jugador con padding si es necesario, son observaciones tipo np.ndarray de forma (30, 14) y los conos de cada jugador
            
    

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
                self.game.screen.blit(s, (x * self.game.cell_size, y * self.game.cell_size))


    def apply_action(self, agent, action):
        player = self.players_dict[agent]

        if action == 0:
            player.change_direction(pygame.Vector2(0, -1))  # Arriba
        elif action == 1:
            player.change_direction(pygame.Vector2(0, 1))   # Abajo
        elif action == 2:
            player.change_direction(pygame.Vector2(-1, 0))  # Izquierda
        elif action == 3:
            player.change_direction(pygame.Vector2(1, 0))   # Derecha
        elif action == 4:
            if random.random() < 0.8:
                player.trailEnabled = not player.trailEnabled  # Toggle trazo

    #Muere todo un equipo
    def team_dead(self, team_name):
        return all(
            player.team == team_name and not player.isAlive
            for player in self.players_dict.values()
            if player.team == team_name
        )

    #Hallar el que consiguio la kill
    def find_killer(self, agent):
        victim = self.players_dict[agent]
        killer = self.game.killed_by.get(victim, None)

        if killer is None:
            return None  # Autodestrucción o muro

        # Invertimos el diccionario players_dict para obtener el nombre del agente
        reverse_dict = {v: k for k, v in self.players_dict.items()}
        return reverse_dict.get(killer, None)  #Nombre del killer
    
    def close(self):
        if self.render_mode == "human":
            pygame.quit()


    def draw(self):
        return self.game.draw()
        

    def build_Obs_Matrix(self): 
            """
            Esta es la informacion completa del juego
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