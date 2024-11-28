import pygame
from constants import screen
from classes.map import map_model

class Home:
    def __init__(self):
        pass

    @staticmethod
    def run():
        screen.fill((30, 30, 30))  # Fundo cinza escuro para contraste
        map_model.draw()
