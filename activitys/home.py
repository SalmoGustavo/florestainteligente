import pygame
from constants import screen
from classes.map import map_model


class Home:
    def __init__(self):
        pass

    @staticmethod
    def run():
        # Preencher o fundo com uma cor sólida (mais clara que a Sidebar)
        bg_color = (25, 25, 55)  # Cor sólida do fundo
        screen.fill(bg_color)

        # Desenhar o mapa sobre o fundo sólido
        map_model.draw()
