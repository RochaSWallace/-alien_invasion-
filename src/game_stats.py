from settings import Settings

class GameStats():
    """Armazena dados estatísticos da Invasão Alienígena."""
    def __init__(self, ai_settings:Settings):
        """Inicializa os dados estatísticos."""
        self.ai_settings = ai_settings
        self.game_active = False
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        """Inicializa os dados estatísticos que podem mudar durante o jogo."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
