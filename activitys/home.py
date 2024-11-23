import pygame
from constants import screen
from classes.map import map_model
from classes.info import info

class Home:
    def __init__(self):
        pass

    @staticmethod
    def run():
        screen.fill((20, 25, 25))
        map_model.draw()
        info.draw()
