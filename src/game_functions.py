import sys
import pygame
from pygame.surface import Surface
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien


def fire_bullet(ai_settings:Settings, screen:Surface, ship:Ship, bullets:Bullet): 
    """Dispara um projétil se o limite ainda não foi alcançado."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings=ai_settings, screen=screen, ship=ship)
        bullets.add(new_bullet)


def check_keydown_events(event, ai_settings:Settings, screen:Surface, ship:Ship, bullets:Bullet):
    """Responde a pressionamentos de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship:Ship):
    """Responde a solturas de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings:Settings, screen:Surface, ship:Ship, bullets:Bullet):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event=event, ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event=event, ship=ship)


def update_screen(ai_settings:Settings, screen:Surface, ship:Ship, bullets:Bullet, alien:Alien):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    alien.blitme()

    pygame.display.flip()


def update_bullets(bullets:Bullet):
    """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
