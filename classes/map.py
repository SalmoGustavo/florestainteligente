import pygame
import requests
from constants import screen, screen_size

pygame.font.init()

class FireFocus:
    next_id = 0

    def __init__(self, position):
        self.id = FireFocus.next_id
        self.position = position
        self.is_active = False
        self.max_radius = 120
        self.min_radius = 100
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
        if active != self.is_active:
            self.is_active = active
            if active:
                requests.get('https://trigger.macrodroid.com/6c3d142f-f648-4c17-8564-ad0f4bc72086/fogo')

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


import requests

class Sidebar:
    def __init__(self):
        self.width = 300
        self.height = screen_size[1]
        self.bg_color = (30, 30, 60)  # Cor sólida da Sidebar
        self.font_color = (255, 255, 255)
        self.font = pygame.font.Font(None, 36)
        self.info_font = pygame.font.Font(None, 28)
        self.title = "Monitoramento"
        self.api_key = "14b7f3ebd1adcc310b334c4f49b3ab47"
        self.city = "Itinga,BR"
        self.weather_info = None
        self.active_fire_focus_count = 0  # Contagem inicial de focos ativos
        self.fetch_weather_data()

    def fetch_weather_data(self):
        """Busca dados climáticos da API OpenWeatherMap."""
        url = f"https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric&lang=pt_br"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                self.weather_info = {
                    "temperature": f"{data['main']['temp']}°C",
                    "humidity": f"{data['main']['humidity']}%",
                    "wind_speed": f"{data['wind']['speed']} m/s",
                    "description": data['weather'][0]['description'].capitalize(),
                }
            else:
                print(f"Erro ao buscar dados climáticos: {response.status_code}")
        except Exception as e:
            print(f"Erro na requisição da API: {e}")

    def set_fire_focus_count(self, count):
        """Atualiza a quantidade de focos de incêndio detectados."""
        self.active_fire_focus_count = count

    def draw(self):
        # Preencher a barra lateral com cor sólida
        sidebar_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(screen, self.bg_color, sidebar_rect)

        # Desenhar o título
        title_surface = self.font.render(self.title, True, self.font_color)
        title_rect = title_surface.get_rect(center=(self.width // 2, 50))
        screen.blit(title_surface, title_rect)

        # Exibir os dados climáticos, se disponíveis
        y_offset = 120
        if self.weather_info:
            info_data = [
                ("Condição", self.weather_info["description"]),
                ("Temperatura", self.weather_info["temperature"]),
                ("Umidade", self.weather_info["humidity"]),
                ("Vento", self.weather_info["wind_speed"]),
                ("Focos ativos", str(self.active_fire_focus_count)),  # Quantidade de focos ativos
            ]

            for label, value in info_data:
                label_surface = self.info_font.render(label, True, self.font_color)
                value_surface = self.info_font.render(value, True, (200, 200, 255))
                label_rect = label_surface.get_rect(left=20, top=y_offset)
                value_rect = value_surface.get_rect(left=20, top=y_offset + 30)
                screen.blit(label_surface, label_rect)
                screen.blit(value_surface, value_rect)
                y_offset += 80
        else:
            # Mensagem de erro, caso os dados não sejam carregados
            error_surface = self.info_font.render("Erro ao carregar dados", True, self.font_color)
            screen.blit(error_surface, (20, y_offset))


class Map:
    def __init__(self):
        self.map_size = (810, 810)
        self.image = pygame.image.load('assets/top-map.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0] / 1.4, self.image.get_size()[1] / 1.4))
        self.rect = self.image.get_rect(center=(screen_size[0] / 2 + 150, screen_size[1] / 2))
        self.fire_focus_points = [FireFocus([854, 276]), FireFocus([1163, 444]), FireFocus([752, 770]),
                                  FireFocus([1217, 709]), FireFocus([1061, 494])]
        self.sidebar = Sidebar()

    def count_active_fire_focus(self):
        """Conta os focos de incêndio ativos."""
        return sum(1 for focus in self.fire_focus_points if focus.is_active)

    def draw(self):
        # Atualizar a quantidade de focos ativos
        active_count = self.count_active_fire_focus()
        self.sidebar.set_fire_focus_count(active_count)

        # Desenhar o mapa e a Sidebar
        screen.blit(self.image, self.rect.topleft)
        self.sidebar.draw()
        for fire_focus in self.fire_focus_points:
            fire_focus.draw()


    def toggle_fire_focus(self, s1, s2, s3, s4):
        print(s1, s2, s3, s4)
        print(bool(s1 == 1 and s3 == 1 and s4 == 1))

        if s1 == 1 and s2 == 1 and s3 == 1:
            self.fire_focus_points[4].toggle(True)
            self.fire_focus_points[0].toggle(False)
            self.fire_focus_points[1].toggle(False)
            self.fire_focus_points[2].toggle(False)
            self.fire_focus_points[3].toggle(False)
            return None
        else:
            self.fire_focus_points[4].toggle(False)

        self.fire_focus_points[0].toggle(s4)
        self.fire_focus_points[1].toggle(s3)
        self.fire_focus_points[2].toggle(s2)
        self.fire_focus_points[3].toggle(s1)


map_model = Map()
