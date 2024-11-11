import pygame
from constants import screen
from classes.map import model

class Home:
    def __init__(self):
        pass

    @staticmethod
    def run():
        screen.fill((255, 255, 255))
        model.draw()
