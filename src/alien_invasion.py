import pygame
from pygame.sprite import Group
import game_functions as gf
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from score_board import ScoreBoard


def run_game():
    pygame.init()
    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    play_button = Button(ai_settings, screen, "Play")
    stats = GameStats(ai_settings)
    score = ScoreBoard(ai_settings, screen, stats)
    ship = Ship(ai_settings=ai_settings, screen=screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, ship, aliens)

    while True:
        gf.check_events(ship=ship, bullets=bullets, ai_settings=ai_settings, screen=screen, stats=stats, play_button=play_button, aliens=aliens)

        gf.update_screen(ai_settings, screen, stats, ship, bullets, aliens, play_button, score)

        if stats.game_active:
            ship.update()

            gf.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, score)

            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)


run_game()
