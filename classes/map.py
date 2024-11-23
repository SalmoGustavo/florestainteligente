import pygame
from constants import screen, screen_size


class FireFocus:
    next_id = 0

    def __init__(self, position):
        self.id = FireFocus.next_id
        self.position = position
        self.is_active = False
        self.max_radius = 100
        self.min_radius = 80
        self.radius = 5
        self.growth_speed = 1
        self.is_expanding = True
        self.surface = self.create_surface()
        self.wave_effect_active = False
        self.wave_radius = 0
        FireFocus.next_id += 1

    def create_surface(self):
        # Superfície maior para suportar a expansão completa da onda
        expanded_size = 4 * self.max_radius
        surface = pygame.Surface((expanded_size, expanded_size), pygame.SRCALPHA)
        surface.set_alpha(128)
        return surface

    def toggle(self):
        self.is_active = not self.is_active

    def draw(self):
        if self.is_active:
            # Limpa a superfície principal
            self.surface.fill((0, 0, 0, 0))

            # Atualiza o raio do círculo principal
            self.update_radius()

            # Desenha o círculo principal no centro da superfície maior
            pygame.draw.circle(self.surface, pygame.Color('red'), (2 * self.max_radius, 2 * self.max_radius),
                               self.radius)

            # Desenha o efeito de ondulação, se ativo
            if self.wave_effect_active:
                self.draw_wave_effect()

            # Blit do círculo no local correto na tela, com ajuste para o centro da superfície maior
            screen.blit(self.surface, (self.position[0] - 2 * self.max_radius, self.position[1] - 2 * self.max_radius))

    def update_radius(self):
        # Modifica o raio para simular expansão e contração
        if self.is_expanding:
            if self.radius < self.max_radius:
                self.radius += self.growth_speed
            else:
                self.is_expanding = False
                self.start_wave_effect()  # Inicia o efeito de ondulação
        else:
            if self.radius > self.min_radius:
                self.radius -= self.growth_speed
            else:
                self.is_expanding = True

    def start_wave_effect(self):
        # Inicia o efeito de ondulação ao atingir o tamanho máximo
        self.wave_effect_active = True
        self.wave_radius = self.radius

    def draw_wave_effect(self):
        # Desenha uma onda que se expande e desaparece
        wave_alpha = max(0, 255 - (self.wave_radius - self.radius) * 5)  # Diminui a opacidade
        wave_surface = pygame.Surface((4 * self.max_radius, 4 * self.max_radius), pygame.SRCALPHA)
        wave_surface.set_alpha(wave_alpha)

        # Desenha o círculo da onda com crescimento rápido e transparência
        pygame.draw.circle(wave_surface, pygame.Color('red'), (2 * self.max_radius, 2 * self.max_radius),
                           self.wave_radius)
        screen.blit(wave_surface, (self.position[0] - 2 * self.max_radius, self.position[1] - 2 * self.max_radius))

        # Expande a onda e desativa o efeito quando a transparência acabar
        self.wave_radius += 2
        if wave_alpha <= 0:
            self.wave_effect_active = False


class Map:
    def __init__(self):
        self.map_size = (810, 810)
        self.image = pygame.image.load('assets/mapa.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], screen_size[1]))
        self.rect = self.image.get_rect(center=(screen_size[0] / 2, screen_size[1] / 2))
        self.rect.bottomright = screen_size
        self.fire_focus_points = [FireFocus([970, 200]), FireFocus([900, 700]), FireFocus([1500, 450])]

    def draw(self):
        screen.blit(self.image, self.rect.topleft)
        for fire_focus in self.fire_focus_points:
            fire_focus.draw()

    def toggle_fire_focus(self, index):
        if 0 <= index < len(self.fire_focus_points):
            self.fire_focus_points[index].toggle()


# Instancia do mapa principal
map_model = Map()
