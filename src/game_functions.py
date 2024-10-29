import sys
import pygame
from pygame.surface import Surface
from pygame.sprite import Group
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


def update_screen(ai_settings:Settings, screen:Surface, ship:Ship, bullets:Group, aliens:Group):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    pygame.display.flip()


def update_bullets(bullets:Bullet):
    """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def get_number_aliens_x(ai_settings:Settings, alien_width:float):
    """Determina o número de alienígenas que cabem em uma linha."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))

    return number_aliens_x


def get_number_rows(ai_settings:Settings, ship_height:int, alien_height:int):
    """Determina o número de linhas com alienígenas que cabem na tela."""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows


def create_alien(ai_settings:Settings, screen:Surface, aliens:Group, alien_number:int, row_number:int):
    """Cria um alienígena e o posiciona na linha"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def change_fleet_direction(ai_settings:Settings, aliens:Group):
    """Faz toda a frota descer e muda a sua direção."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
        ai_settings.fleeet_direction *= -1


def check_fleet_edges(ai_settings:Settings, aliens:Group):
    """Responde apropriadamente se algum alienígena alcançou uma borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def update_aliens(ai_settings:Settings, aliens:Group):
    """Atualiza as posições de todos os alienígenas da frota."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


def create_fleet(ai_settings:Settings, screen:Surface, ship:Ship, aliens:Group):
    """Cria uma frota completa de alienígenas."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, number_row)
