import sys
from time import sleep
import pygame
from pygame.surface import Surface
from pygame.sprite import Group
from ship import Ship
from settings import Settings
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard


def fire_bullet(ai_settings:Settings, screen:Surface, ship:Ship, bullets:Bullet):
    """Dispara um projétil se o limite ainda não foi alcançado."""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings=ai_settings, screen=screen, ship=ship)
        bullets.add(new_bullet)


def check_play_keydown(ai_settings:Settings, screen:Surface, stats:GameStats, ship:Ship, aliens:Group, bullets:Group, score:ScoreBoard):
    if not stats.game_active:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        
        score.prep_score()
        score.prep_high_score()
        score.prep_level()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_keydown_events(event, ai_settings:Settings, screen:Surface, ship:Ship, bullets:Bullet, stats:GameStats, aliens:Group, score:ScoreBoard):
    """Responde a pressionamentos de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()

    elif event.key == pygame.K_p:
        check_play_keydown(ai_settings, screen, stats, ship, aliens, bullets, score)


def check_keyup_events(event, ship:Ship):
    """Responde a solturas de tecla."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_play_button(ai_settings:Settings, screen:Surface, stats:GameStats, score:ScoreBoard, play_button:Button, ship:Ship, aliens:Group, bullets:Group, mouse_x, mouse_y):
    """Inicia um novo jogo quando o jogador clicar em Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True

        score.prep_score()
        score.prep_high_score()
        score.prep_level()
        score.prep_ships()

        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_events(ai_settings:Settings, screen:Surface, stats:GameStats, play_button:Button, ship:Ship, bullets:Bullet, aliens:Group, score:ScoreBoard):
    """Responde a eventos de pressionamento de teclas e de mouse."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event=event, ai_settings=ai_settings, screen=screen, ship=ship, bullets=bullets, stats=stats, aliens=aliens, score=score)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event=event, ship=ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, score, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def update_screen(ai_settings:Settings, screen:Surface, stats:GameStats, ship:Ship, bullets:Group, aliens:Group, play_button:Button, score:ScoreBoard):
    """Atualiza as imagens na tela e alterna para a nova tela."""
    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    score.show_score()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()


def check_bullet_alien_collisions(ai_settings:Settings, screen:Surface, ship:Ship, aliens:Group, bullets:Group, stats:GameStats,score:ScoreBoard):
    """Responde a colisões entre projéteis e alienígenas."""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            check_high_score(stats, score)
            score.prep_score()

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        score.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)


def update_bullets(ai_settings:Settings, screen:Surface, ship:Ship, aliens:Group, bullets:Group, stats:GameStats, score:ScoreBoard):
    """Atualiza a posição dos projéteis e se livra dos projéteis antigos."""
    bullets.update()
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, score)

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


def check_fleet_edges(ai_settings:Settings, aliens:Group):
    """Responde apropriadamente se algum alienígena alcançou uma borda."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            ai_settings.fleet_direction *= -1
            break


def update_aliens(ai_settings:Settings, stats:GameStats, screen:Surface, ship:Ship, aliens:Group, bullets:Group, score:ScoreBoard):
    """Atualiza as posições de todos os alienígenas da frota."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets, score)

    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, score)


def create_fleet(ai_settings:Settings, screen:Surface, ship:Ship, aliens:Group):
    """Cria uma frota completa de alienígenas."""
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, number_row)


def ship_hit(ai_settings:Settings, stats:GameStats, screen:Surface, ship:Ship, aliens:Group, bullets:Group, score:ScoreBoard):
    """Responde ao fato de a espaçonave ter sido atingida por um alienígena."""
    if stats.ships_left > 0:
        stats.ships_left -= 1
        score.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings:Settings, stats:GameStats, screen:Surface, ship:Ship, aliens:Group, bullets:Group, score:ScoreBoard):
    """Verifica se algum alienígena alcançou a parte inferior da tela."""
    screen_rect = screen.get_rect()

    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets, score)
            break


def check_high_score(stats:GameStats, score:ScoreBoard):
    """Verifica se há uma nova pontuação máxima."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        score.prep_high_score()
