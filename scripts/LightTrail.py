import pygame
import time
from player import Player

class LightTrail:
    def __init__(self, player, color):
#        self.player = player
#        self.color = pygame.Color(color)
#        self.lightPoints = []   #guarda los trazos de luz (posiciones y tiempo)
#        self.radius = 5
#        self.size = 60

        ####Codigo comentado si se quiere dejar por tiempo
        self.player = player
        self.color = pygame.Color(color)
        self.lightPoints = [] #guarda los trazos de luz (posiciones y tiempo)
        self.duration = 10 #numero de segundos que tarda en desaparecer  
        ####
        

    def updateTrail(self):
#        pos = (int(self.player.old_position.x),int(self.player.old_position.y))
#        self.lightPoints.append(pos)

#        if len(self.lightPoints) > self.size:
#            self.lightPoints.pop(0)
            
        ####
        if self.player.getTrailEstate():  #Solo guardar la posición si la estela está encendida
                current_time = time.time()
                pos = (int(self.player.old_position.x), int(self.player.old_position.y), current_time)
                self.lightPoints.append(pos)

                #para filtrar los rastros que deben desaparecer:
                self.lightPoints = [
                (x,y,t) for (x,y,t) in self.lightPoints if current_time - t <self.duration
                ]
        ####

    def drawTrail(self, screen,cell_size):
#        for x, y in self.lightPoints:           #convierte cada casilla a pixeles para dibujarlo correctamente
#            px = x * cell_size
#            py = y * cell_size
#            pygame.draw.rect(screen, self.color, (px, py, cell_size, cell_size))

        ####
        current_time = time.time()
        for x, y, t in self.lightPoints:
            transparency = max(0, 255 - int(255 * ((current_time - t) / self.duration)))   #Hace que el bloque se vea más "difuso" en vez de desaparecer de golpe con el tiempo
            faded_color = pygame.Color(self.color.r, self.color.g, self.color.b, self.color.a)
            faded_color.a = transparency

            s = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)    #se usa para dibujar el trazo desvaneciendose
            pygame.draw.rect(s, faded_color, (0, 0, cell_size, cell_size))
            screen.blit(s, (x * cell_size, y * cell_size))
        ####




        