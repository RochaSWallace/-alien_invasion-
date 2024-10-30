import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_settings=ai_settings, screen=screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ship=ship, bullets=bullets, ai_settings=ai_settings, screen=screen)

        ship.update()

        gf.update_bullets(ai_settings, screen, ship, aliens, bullets)

        gf.update_aliens(ai_settings, ship, aliens)

        gf.update_screen(ai_settings, screen, ship, bullets, aliens)


run_game()
