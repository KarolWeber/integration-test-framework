import allure
from api.clients.admin_client.casino_client import CasinoClient
from entities.backoffice.casino.game_reporting_groups.game_reporting_group_list import \
    GameReportingGroupsList
from entities.backoffice.casino.games.game_providers_list import \
    GameProviderList
from entities.backoffice.casino.games.games_list import GamesList
from utils.logging.logger import StepLogger


class CasinoService:
    """
    Serwis do obsługi funkcji kasyna w backoffice.

    Umożliwia dostęp do:
        - gier (GamesService),
        - dostawców gier (GameProvidersService),
        - grup raportowych gier (GameReportingGroups).
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis kasyna.

        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context
        self.game_providers = GameProvidersService(self._context)
        self.games = GamesService(self._context)
        self.game_reporting_groups = GameReportingGroups(self._context)


class GamesService:
    """
    Serwis do zarządzania grami w backoffice.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context

    @allure.step("Admin get games list")
    def list(self, provider=None, limit=2000, visible=None, name=None,
             game_id=None, free_spins=None, step=True):
        """
        Pobiera listę gier z systemu.

        :param provider: Obiekt dostawcy gry.
        :param limit: (int) Maksymalna liczba gier do pobrania.
        :param visible: (bool) Filtrowanie po widoczności gry.
        :param name: (str) Filtrowanie po nazwie gry.
        :param game_id: (str) Filtrowanie po ID gry.
        :param free_spins: (bool) Filtrowanie po wsparciu free spinów.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca listę obiektów gier
        """
        if provider:
            provider = self._context.casino.game_providers.list(provider=provider, step=False)
        resp = CasinoClient.Game.list(self._context, provider=provider, limit=limit, visible=visible, name=name, game_id=game_id,
                                      free_spins=free_spins)
        if step:
            StepLogger.log_step("ADMIN GET GAMES LIST", response=resp)
        if resp.status_code != 200:
            return resp
        games_list = GamesList.from_dict(resp.json())

        return games_list

    @allure.step("Admin change game reporting group")
    def change_reporting_group(self, game, group_name, step=True):
        """
        Zmienia grupę raportową gry

        :param game: Obiekt gry
        :param group_name: (str) Nazwa grupy: group.slot_games, group.cylinder_games, group.card_games_no_poker, group.dice_games
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        """
        rep_groups = self._context.casino.game_reporting_groups.list(step=False)
        group = next((g for g in rep_groups if g.name == group_name), None)
        if group is None:
            raise ValueError(f"Group {group_name} not found")
        payload = {
            "gameId": game.id,
            "reportingGameGroup": group.id
        }
        resp = CasinoClient.Game.change_reporting_group(self._context, payload=payload)
        if step:
            StepLogger.log_step(f"ADMIN CHANGE GAME REPORTING GROUP: {game.name} → {group.name}", response=resp)
        return resp

    @allure.step("Admin change game visibility")
    def change_visibility(self, games, is_visible, step=True):
        """
        Zmienia widoczność jednej lub wielu gier.

        :param games: Obiekt gry lub lista obiektów gier.
        :param is_visible: (bool) Nowa wartość widoczności.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        """
        payload = []
        games_name = []
        if isinstance(games, list):
            for g in games:
                payload.append({"id": g.id, "isVisible": is_visible})
                games_name.append(g.name)
        else:
            payload.append({"id": games.id, "isVisible": is_visible})
            games_name.append(games.name)
        resp = CasinoClient.Game.change_visibility(self._context, payload=payload)
        if step:
            StepLogger.log_step(f"ADMIN CHANGE GAME VISIBILITY: {games_name} → {is_visible}", response=resp)
        return resp


class GameProvidersService:
    """
    Serwis do zarządzania dostawcami w backoffice.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context

    @allure.step("Admin sync games")
    def sync_games(self, provider):
        """
        Synchronizuje gry wybranego dostawcy

        :param provider: (str) Nazwa dostawcy
        """
        provider = self._context.casino.game_providers.list(provider=provider, step=False)
        payload = {'providerId': provider.id}
        return CasinoClient.Providers.sync_games(self._context, payload=payload, provider_name=provider.name)

    @allure.step("Admin get providers list")
    def list(self, provider=None, step=True):
        """
        pobiera listę dostawców gier

        :param provider: (str, opcjonalny) Nazwa dostawcy.
        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Listę obiektów dostawców gier lub obiekt dostawcy jeśli została podana nazwa dostawcy
        """
        resp = CasinoClient.Providers.get(self._context)
        if step:
            StepLogger.log_step("ADMIN GET PROVIDERS LIST", response=resp)
        if resp.status_code != 200:
            return resp
        game_provider_list = GameProviderList.from_dict(resp.json())
        if provider:
            return next((p for p in game_provider_list if p.name == provider), [])
        return game_provider_list


class GameReportingGroups:
    """
    Serwis do zarządzania grupami raportowymi gier w backoffice.
    """

    def __init__(self, context):
        """
        :param context: Obiekt kontekstu zalogowanego administratora.
        """
        self._context = context

    @allure.step("Admin get game reporting groups list")
    def list(self, step=True):
        """
        Pobiera listę grup raportowych.

        :param step: (bool) Flaga logowania kroku 'StepLogger'.
        :return: Zwraca listę obiektów grup raportowych.
        """
        resp = CasinoClient.ReportingGroups.get(self._context)
        if step:
            StepLogger.log_step("ADMIN GET GAME REPORTING GROUPS LIST", response=resp)
        if resp.status_code != 200:
            return resp
        resp = GameReportingGroupsList.from_dict(resp.json())
        return resp
