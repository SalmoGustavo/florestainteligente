import pygame
import platform
import ctypes

def set_dpi():
    if platform.system() == "Windows":
        try:
            # Windows 10 ou Superior
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception as e:
            print(e)
            try:
                # Windows 8.1 ou Superior
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception as e:
                print(e)

set_dpi()

# Screen Settings

pygame.display.init()
pygame.display.set_caption('Floresta Inteligente - 2° EMTI 1')
screen_size = pygame.display.get_desktop_sizes()[0]
screen_size = (screen_size[0] / 1.04, screen_size[1] / 1.1)
screen = pygame.Surface(screen_size)
display = pygame.display.set_mode(screen_size)

# Clock

clock = pygame.time.Clock()
FPS = 60
