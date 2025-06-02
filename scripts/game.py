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

        self.screen = pygame.display.set_mode((1280, 720))
        self.cell_size = 40 #la casilla es de 40x40 pixeles
        self.grid_cols = self.screen.get_width() // self.cell_size  #cambiado a columnas
        self.grid_rows = self.screen.get_height() // self.cell_size #cambiado a filas

        self.player1 = Player(2, 9, self.screen, "RED", self.cell_size, self.mapping_player1)
        self.player2 = Player(29, 9, self.screen, "BLUE", self.cell_size, self.mapping_player2)

        self.trail1 = LightTrail(self.player1, "RED")
        self.trail2 = LightTrail(self.player2, "BLUE")

        self.obs = np.zeros((8, self.grid_rows, self.grid_cols), dtype=np.float32) #crea una matriz de ceros con 8 niveles/dimensiones, y con ancho y alto del mapa ((1280, 720))


        self.clock = pygame.time.Clock()
        self.running = True



        

    
    
    def update_state(self):

#        self.build_Obs_Matrix()

        self.trail1.updateTrail()
        self.trail2.updateTrail()

        self.trail1.drawTrail(self.screen, self.cell_size)
        self.trail2.drawTrail(self.screen, self.cell_size)
        

        # Actualizamos el movimiento de cada jugador con su propias teclas
        dt = self.clock.tick(60)
        self.player1.move(dt)
        self.player2.move(dt)

        

#    def build_Obs_Matrix(self): 
#        self.obs.fill(0)  #elimina rastros de frames anteriores 

        #Nivel 0 (Bordes)
#       self.obs[0, 0, :] = 1.0 #en el nivel 0 llenará la fila 0 y todas las columnas de 1's, (parte superior del tablero)
#        self.obs[0, -1, :] = 1.0 #en el nivel 0 llenará la última fila y todas las columnas de 1's (parte inferior del tablero)
#        self.obs[0, :, 0] = 1.0 #primera columna del tablero
#        self.obs[0, :, -1] = 1.0 #última columna del tablero

        #Nivel 1 (player 1)
#        x1 = int(self.player1.position.x)
#        y1 = int(self.player1.position.y)
#        self.obs[1, y1, x1] = 1.0 #en el nivel 1 llenará de 1's las posiciones x e y de player 1 (las filas son las Y en el plano)

        #Nivel 2 (player 2)
#        x2 = int(self.player2.position.x)
#        y2 = int(self.player2.position.y)
#        self.obs[2, y2, x2] = 1.0 #en el nivel 2 llenará de 1's las posiciones x e y de player 2

        #Nivel 3 (Trzo de luz)
#        for pos in self.trail1.lightPoints + self.trail2.lightPoints:  #recorre ambas posiciones de las matrices una al aldo de la otra concatenadas peor primero recorre las de p1 y luego de p2
#            lx = int(pos[0])                                   #las X de la luz (0 poruqe ahí está X en la coordenada pos)
#            ly = int(pos[1])                                   #Las Y de la luz  (1 porque aí está Y en la coordenada pos)           
#            if 0 <= ly < self.grid_height and 0 <= lx < self.grid_width:      #asegura que las coordenadas estén dentro de tamaño de la matriz (tamaño de tablero) y llena de 1's esas posiciones
#                self.obs[3, ly, lx] = 1.0
        
        #Nivel 4 (dirección x de player 1) 
#        self.obs[4, y1, x1] = self.player1.direction.x  #Pone la dirección del p1 en x en su posición
        
        #Nivel 5 (dirección y de player 1)
#        self.obs[5, y1, x1] = self.player1.direction.y  #Pone la dirección del p1 en y en su posición

        #Nivel 6 (dirección x de player 2) 
#        self.obs[6, y2, x2] = self.player2.direction.x  #Pone la dirección del p2 en x en su posición
        
        #Nivel 7 (dirección y de player 2)
#        self.obs[7, y2, x2] = self.player2.direction.y 
