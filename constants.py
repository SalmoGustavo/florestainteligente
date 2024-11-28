import pygame
import platform
import ctypes

def set_dpi():
    if platform.system() == "Windows":
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception as e:
            print("DPI Awareness Error:", e)
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except Exception as e:
                print("Fallback DPI Error:", e)

set_dpi()

# Screen Settings
pygame.display.init()
pygame.display.set_caption('Floresta Inteligente - 2° EMTI 1')

# Ajustando a resolução
screen_size = (int(pygame.display.Info().current_w * 0.9), int(pygame.display.Info().current_h * 0.9))
screen = pygame.Surface(screen_size)
display = pygame.display.set_mode(screen_size)

# Clock
clock = pygame.time.Clock()
FPS = 60
