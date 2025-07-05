from pettingzoo.utils import ParallelEnv
from gymnasium import spaces
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
        self.agents = ['player1', 'player2', 'player3', 'player4']
        self.num_agents = len(self.agents)
        self.possible_agents = self.agents.copy()
        self.max_num_agents = 4
        self.observation_space = {
            agent: spaces.Box(low=0, high=1, shape=(30, 14), dtype=np.float32)  # 30 casillas visibles (coordenadas del cono de visión), 14 canales
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
    def observe(self, agent):
       # genera el cono de visión para el agente (debe generar la matriz de obstaculos también)       
       # luego genera el tensor de observación y con pad_observation() asegura que tenga una longitud fija 
       # retorna el tensor de observación con la longitud fija
        return pad_observation(obs_visible)

    #aparentemente hay que mover get_obs_in_vision()  y get_obstacles_from_obs() a la clase TronParallelEnv para que funcione con el entorno paralelo