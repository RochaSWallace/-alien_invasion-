import sys
import pygame
from ship import Ship
from settings import Settings


def check_events(ship:Ship):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = True

            elif event.key == pygame.K_LEFT:
                ship.moving_left = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ship.moving_right = False

            elif event.key == pygame.K_LEFT:
                ship.moving_left = False


def update_screen(ai_settings:Settings, screen:pygame.surface.Surface, ship:Ship):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    pygame.display.flip()
    