import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from settings import Settings
from ship import Ship

class Bullet(Sprite):
    """Uma classe que administra projéteis disparados pela espaçonave"""
    def __init__(self, ai_settings:Settings, screen:Surface, ship:Ship):
        """Cria um objeto para o projétil na posição atual da espaçonave."""
        super().__init__()
        self.screen = screen
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """Move o projétil para cima na tela."""
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        """Desenha o projétil na tela"""
        pygame.draw.rect(self.screen, self.color, self.rect)
    