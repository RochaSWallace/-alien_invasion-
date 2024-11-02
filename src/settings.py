"""Não foi necessário nenhuma lib externa para criação desta Classe"""
class Settings():
    """
    Uma classe para armazenar todas as configurações da Invasão
Alienígena.
    """
    def __init__(self):
        """Inicializa as configurações do jogo"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)
        # self.ship_speed_factor = 1
        self.ship_limit = 3
        # self.bullet_speed_factor = 1
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3
        # self.alien_speed_factor = 1
        self.fleet_drop_speed = 5
        self.fleet_direction = 1
        self.speed_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Inicializa as configurações que mudam no decorrer do jogo."""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 1
        self.alien_points = 50

    def increase_speed(self):
        """Aumenta as configurações de velocidade."""
        self.ship_speed_factor *= self.speed_scale
        self.bullet_speed_factor *= self.speed_scale
        self.alien_speed_factor *= self.speed_scale
        self.alien_points *= self.score_scale
