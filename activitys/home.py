import pygame
from constants import screen
from classes.map import map_model
from classes.info import info

class Home:
    def __init__(self):
        pass

    @staticmethod
    def run():
        screen.fill((250, 50, 50))
        map_model.draw()
        info.draw()
