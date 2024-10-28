import pygame
from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    conf = Settings()

    screen = pygame.display.set_mode((conf.screen_width, conf.screen_height))
    pygame.display.set_caption("Alien Invasion")
    ship = Ship(screen=screen)

    while True:
        gf.check_events(ship=ship)

        ship.update()

        gf.update_screen(ai_settings=conf, screen=screen, ship=ship)


run_game()
