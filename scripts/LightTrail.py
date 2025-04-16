import pygame
from player import Player

class LightTrail:
    def __init__(self, player, color):
        self.player = player
        self.color = color
        self.lightPoints = []
        self.radius = 5
        self.size = 60
        
    def updateTrail(self):
        pos = (int(self.player.position.x),int(self.player.position.y))
        self.lightPoints.append(pos)

        if len(self.lightPoints) > self.size:
            self.lightPoints.pop(0)


    def drawTrail(self, screen):
        for point in self.lightPoints:
            pygame.draw.circle(screen, self.color, point, self.radius)




        