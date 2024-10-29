import pygame
from pygame.sprite import Sprite
from settings import Settings
from pygame.surface import Surface


class Alien(Sprite):
    """Uma classe que representa um único alienígena da frota."""
    def __init__(self, ai_settings:Settings, screen:Surface):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("src/images/navio_marinha.bmp")
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        """Desenha o alienígena em sua posição atual."""
        self.screen.blit(self.image, self.rect)
    