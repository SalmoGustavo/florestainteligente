import pygame
from constants import screen, screen_size

pygame.font.init()

class FireFocus:
    next_id = 0

    def __init__(self, position):
        self.id = FireFocus.next_id
        self.position = position
        self.is_active = False
        self.max_radius = 80
        self.min_radius = 60
        self.radius = 5
        self.growth_speed = 1
        self.is_expanding = True
        self.surface = self.create_surface()
        self.wave_effect_active = False
        self.wave_radius = 0
        FireFocus.next_id += 1

    def create_surface(self):
        expanded_size = 4 * self.max_radius
        surface = pygame.Surface((expanded_size, expanded_size), pygame.SRCALPHA)
        surface.set_alpha(128)
        return surface

    def toggle(self, active):
        self.is_active = active

    def draw(self):
        if self.is_active:
            self.surface.fill((0, 0, 0, 0))
            self.update_radius()

            pygame.draw.circle(self.surface, pygame.Color('red'), (2 * self.max_radius, 2 * self.max_radius),
                               self.radius)

            if self.wave_effect_active:
                self.draw_wave_effect()

            screen.blit(self.surface, (self.position[0] - 2 * self.max_radius, self.position[1] - 2 * self.max_radius))

    def update_radius(self):
        if self.is_expanding:
            if self.radius < self.max_radius:
                self.radius += self.growth_speed
            else:
                self.is_expanding = False
                self.start_wave_effect()
        else:
            if self.radius > self.min_radius:
                self.radius -= self.growth_speed
            else:
                self.is_expanding = True

    def start_wave_effect(self):
        self.wave_effect_active = True
        self.wave_radius = self.radius

    def draw_wave_effect(self):
        wave_alpha = max(0, 255 - (self.wave_radius - self.radius) * 5)
        wave_surface = pygame.Surface((4 * self.max_radius, 4 * self.max_radius), pygame.SRCALPHA)
        wave_surface.set_alpha(wave_alpha)

        pygame.draw.circle(wave_surface, pygame.Color('orange'), (2 * self.max_radius, 2 * self.max_radius),
                           self.wave_radius)
        screen.blit(wave_surface, (self.position[0] - 2 * self.max_radius, self.position[1] - 2 * self.max_radius))

        self.wave_radius += 2
        if wave_alpha <= 0:
            self.wave_effect_active = False


class Sidebar:
    def __init__(self):
        self.width = 300
        self.height = screen_size[1]
        self.bg_color = (30, 30, 60)
        self.font_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 28)
        self.title = "Monitoramento"
        self.info = [
            ("Focos de incêndio", "🔥 5"),
            ("Temperatura média", "🌡️ 35°C"),
            ("Umidade", "💧 40%"),
            ("Velocidade do vento", "🌬️ 15 km/h"),
        ]

    def draw(self):
        sidebar_surface = pygame.Surface((self.width, self.height))
        for y in range(self.height):
            grad_color = (30 + y // 20, 30, 80 + y // 40)
            pygame.draw.line(sidebar_surface, grad_color, (0, y), (self.width, y))
        screen.blit(sidebar_surface, (0, 0))

        title_surface = self.font.render(self.title, True, self.font_color)
        title_rect = title_surface.get_rect(center=(self.width // 2, 50))
        screen.blit(title_surface, title_rect)

        y_offset = 120
        for label, value in self.info:
            label_surface = self.info_font.render(label, True, self.font_color)
            value_surface = self.info_font.render(value, True, (200, 200, 255))
            label_rect = label_surface.get_rect(left=20, top=y_offset)
            value_rect = value_surface.get_rect(left=20, top=y_offset + 30)
            screen.blit(label_surface, label_rect)
            screen.blit(value_surface, value_rect)
            y_offset += 80


class Map:
    def __init__(self):
        self.map_size = (810, 810)
        self.image = pygame.image.load('assets/background-2.jpg')
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], screen_size[1]))
        self.rect = self.image.get_rect(center=(screen_size[0] / 2 + 150, screen_size[1] / 2))
        self.fire_focus_points = [FireFocus([1118, 253]), FireFocus([1600, 424]), FireFocus([1159, 682]),
                                  FireFocus([1627, 709]), FireFocus([1425, 385])]
        self.sidebar = Sidebar()

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        self.sidebar.draw()
        for fire_focus in self.fire_focus_points:
            fire_focus.draw()

    def toggle_fire_focus(self, s1, s2, s3, s4):
        if s1 and s2 and s3:
            self.fire_focus_points[4].toggle(True)
            self.fire_focus_points[0].toggle(False)
            self.fire_focus_points[1].toggle(False)
            self.fire_focus_points[2].toggle(False)
            self.fire_focus_points[3].toggle(False)
            return None
        else:
            self.fire_focus_points[4].toggle(False)

        self.fire_focus_points[0].toggle(s1)
        self.fire_focus_points[1].toggle(s2)
        self.fire_focus_points[2].toggle(s3)
        self.fire_focus_points[3].toggle(s4)


map_model = Map()
