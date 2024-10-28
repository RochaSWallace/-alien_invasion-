import pygame
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(ai_settings=ai_settings, screen=screen)

    while True:
        gf.check_events(ship=ship)

        ship.update()

        gf.update_screen(ai_settings=ai_settings, screen=screen, ship=ship)


run_game()
