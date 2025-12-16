import allure
from api.clients.player_client.game_client import GameClient
from utils.logging.logger import StepLogger


class GameSession:
    def __init__(self, player, game, player_bonus):
        """
        Inicjalizuje sesję gry

        :param player: Obiekt kontekstu zalogowanego gracza.
        :param game: Obiekt gry.
        """
        self.player = player
        self.game = game
        self.player_bonus = player_bonus
        self.status = None
        self.error_code = None
        self.init_token = None
        self.player_external_id = None
        self.current_balance = None
        self.free_spin_id = None
        self.url = None
        self.history = []
        self.authenticate_status = None

    def _set_session_data(self, response):
        """
        Ustawia parametry sesji po inicjalizacji gry.
        """
        if response.status_code == 200:
            data = response.json()
            self.status = data.get("success")
            self.error_code = data.get("errorCodes")
            self.init_token = data.get("token")
            self.player_external_id = data.get("playerExternalId")
        else:
            self.status = False
            self.error_code = response

    @allure.step("Player run game")
    def init_game(self, free_spins_external_id, player_bonus):
        """
        Inicjalizuje grę.

        :param player_bonus: Obiekt bonusu gracza.
        :param free_spins_external_id: (uuid, opcjonalny) Identyfikator bonusu free spin przypisany graczowi.
        """
        resp = GameClient.init_token(player=self.player, game=self.game, player_bonus=self.player_bonus)
        StepLogger.log_step(f"PLAYER RUN GAME: {self.player.email} → {self.game.name}", response=resp)
        if free_spins_external_id:
            self.free_spin_id = free_spins_external_id
        self._set_session_data(resp)
