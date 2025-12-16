import allure
from api.clients.player_client.game_client import GameClient
from api.services.providers_services.provider_one_service import ProviderOneService
from utils.logging.logger import StepLogger


class GameService:
    """
    Serwis do obsługi konta gier przez gracza.
    """

    def __init__(self, context):

        self._context = context

    @allure.step("Player run game")
    def run_game(self, game, free_spins_external_id=None, auto_auth=True, player_bonus=None):
        """
        Uruchamia grę.

        :param game: Obiekt gry.
        :param free_spins_external_id: (uuid, opcjonalny) Identyfikator bonusu free spin przypisany graczowi.
        :param auto_auth: (bool) Flaga ustawiająca automatyczną autentykacji na grze.
        :param player_bonus: (Opcjonalny) Objekt bonusu gracza który będzie rozgrywany na grze.
        :return: Zwraca kontekst sesji gracza na podanej grze.
        """
        if game.provider_name in ("ProviderOneWFS", "ProviderOneProviderFS"):
            return ProviderOneService(self._context, game=game, free_spins_external_id=free_spins_external_id, auto_auth=auto_auth, player_bonus=player_bonus)

    @allure.step("Player run game demo")
    def run_demo(self, game):
        """
        Uruchamia sesję demo gry.
        :param game: Obiekt gry, parametr 'hasDemo' obieku musi być ustawiony na True.
        :return: Zwraca URL do rozgrywki demo.
        """
        resp = GameClient.demo(self._context, game=game)
        StepLogger.log_step(f"PLAYER RUN DEMO GAME >{game.name}<", response=resp)
        if resp.status_code != 200:
            return resp
        return resp.json()['url']
