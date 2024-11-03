import pygame
from pygame.sprite import Sprite
from pygame.surface import Surface
from settings import Settings


class Ship(Sprite):
    def __init__(self, ai_settings:Settings, screen:Surface) -> None:
        """inicializa a espaçonave e define sua posição inical"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.image = pygame.image.load("src/images/sunny.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Atualiza a posição da espaçonave de acordo com a flag de movimento."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor

        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        """Desenha a espaçonave em sua posição atual."""
        self.screen.blit(self.image, self.rect)

    def  center_ship(self):
        """Centraliza a espaçonave na tela."""
        self.center = self.screen_rect.centerx 
        