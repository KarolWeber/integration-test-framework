import allure
from api.clients.admin_client.player_client import PlayersClient
from entities.backoffice.players.player_bonuses_list import \
    PlayerCurrentBonusesList
from entities.backoffice.players.player_wallet_activity_log import \
    PlayerWalletActivityLogList
from utils.logging.logger import StepLogger


class PlayersService:
    """
    Serwis do obsługi graczy w backoffice.
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis graczy.

        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context
        self.bonuses = PlayerBonusesService(self._context)
        self.wallet = PlayerWalletService(self._context)


class PlayerBonusesService:
    """
    Serwis do zarządzania bonusami gracza.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context

    @allure.step("Admin get player bonuses")
    def current_bonuses(self, player, bonus=None, step=True):
        """
        Pobiera listę bonusów przypisanych do gracza.

        :param player: Obiekt gracza
        :param bonus: Opcjonalny Obiekt bonusu
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Listę obiektów bonusów gracza bądź ten podany w 'bonus'
        """
        resp = PlayersClient.Bonuses.bonuses(self._context, player=player)
        if step:
            StepLogger.log_step(f"ADMIN GET PLAYER BONUSES: {player.email}", response=resp)
        if resp.status_code != 200:
            return resp
        bonuses = PlayerCurrentBonusesList.from_dict(resp.json())
        if bonus is None:
            return bonuses
        return next((b for b in bonuses if b.bonus_definition_id == bonus.id), None)


class PlayerWalletService:
    """
    Serwis do zarządzania portfelem gracza.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context

    def activity(self, player):
        """
        Pobiera aktywność portfela gracza

        :param player: Obiekt gracza
        :return: Zwraca listę obiektów aktywności gracza
        """
        resp = PlayersClient.Wallet.activity(self._context, player=player, limit=100)
        if resp.status_code != 200:
            return resp
        return PlayerWalletActivityLogList.from_dict(resp.json())
