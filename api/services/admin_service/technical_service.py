import allure
from api.clients.admin_client.casino_client import CasinoClient
from api.clients.admin_client.technical_client import TechnicalClient
from entities.backoffice.casino.game_reporting_groups.game_reporting_group_list import \
    GameReportingGroupsList
from utils.logging.logger import StepLogger
from utils.mappers.mappers import GAME_TYPE_MAP
from utils.payloads import admin_payloads


class TechnicalService:
    """
    Serwis do obsługi zadań technicznych w backoffice wykorzystywanych tylko do testów.
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis techniczny.

        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context
        self.game = GameService(self._context)
        self.bonus = BonusService(self._context)


class GameService:
    def __init__(self, context):
        """
        Serwis techniczny do zarządzania grami w backoffice.
        """
        self._context = context
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """

    @allure.step("Admin create custom game")
    def create_custom_game(self, game_provider="ProviderOneWFS", game_type="SLOTS", name=None, free_spins_supported=True):
        """
        Tworzy i zwraca grę techniczną.

        :param game_provider: (str) Nazwa dostawcy gier.
        :param game_type: (str) Typ gry.
        :param name: (str, opcjonalny) Nazwa gry.
        :param free_spins_supported: (bool) Flaga określająca czy gra ma free spiny.
        :return: Zwraca obiekt utworzonej gry.
        """

        provider_data = next((provider for provider in self._context.casino.game_providers.list() if provider.name == game_provider), None)
        if provider_data is None:
            raise ValueError(f"Provider {game_provider} not found")
        game_reporting_group_id = None

        game_info = GAME_TYPE_MAP.get(game_type.upper())
        resp = CasinoClient.ReportingGroups.get(self._context)
        reporting_groups = GameReportingGroupsList.from_dict(resp.json())
        for group in reporting_groups:
            if group.name == game_info['group']:
                game_reporting_group_id = group.id
                break

        payload = admin_payloads.create_custom_game_payload(
            provider=provider_data,
            game_reporting_group_id=game_reporting_group_id,
            game_type=game_type,
            name=name,
            free_spins_supported=free_spins_supported
        )

        resp = TechnicalClient.Game.create_custom_game(self._context, payload)
        StepLogger.log_step(f"ADMIN CREATE CUSTOM GAME: {payload['name']}", response=resp)
        if resp.status_code != 200:
            return resp
        game = self._context.casino.games.list(game_id=resp.json()['id'])[0]
        return game

    @allure.step("Admin delete game")
    def remove_game(self, game, step=True):
        """
        Usuwa podaną grę.

        :param game: Obiekt gry
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        """
        payload = {"gameId": game.id}
        resp = TechnicalClient.Game.delete_custom_game(self._context, payload=payload)
        if step:
            StepLogger.log_step(f"ADMIN DELETE CUSTOM GAME {game.name}", response=resp)
        return resp


class BonusService:
    def __init__(self, context):
        """
        Serwis techniczny do zarządzania bonusami w backoffice.
        """
        self._context = context
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """

    @allure.step("Admin delete bonus")
    def delete(self, bonus, step=True):
        """
        Usuwa podany bonus.

        :param bonus: Obiekt bonusu
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        """
        payload = {"id": bonus.id}
        resp = TechnicalClient.Bonus.delete_bonus(self._context, payload=payload)
        if step:
            StepLogger.log_step(f"ADMIN DELETE BONUS {bonus.name}", response=resp)
        return resp
