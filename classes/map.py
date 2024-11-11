import pygame
from constants import screen
from constants import screen_size

class FireFocus:
    ffid = 0
    def __init__(self, pos):
        self.ffid = FireFocus.ffid
        self.pos = pos
        self.active = False
        self.radius = 80
        FireFocus.ffid += 1

    def turn(self):
        self.active = not self.active

    def draw(self):
        if self.active:
            pygame.draw.circle(screen, pygame.Color('red'), self.pos, self.radius)

class Map:
    def __init__(self):
        self.size = [810, 810]
        self.rect = pygame.Rect(0, 0, self.size[0], self.size[1])
        self.rect.centerx, self.rect.centery = screen_size[0] / 2, screen_size[1] / 2

        self.fireFocus = [FireFocus([200, 200]),
                          FireFocus([500, 500])]

    def draw(self):
        pygame.draw.rect(screen, pygame.Color('green'), self.rect)
        for fire_focus in self.fireFocus:
            fire_focus.draw()

    def setFireFocus(self, fireIndex):
        self.fireFocus[fireIndex].turn()

model = Map()
