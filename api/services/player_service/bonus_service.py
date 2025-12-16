import allure
from api.clients.player_client.bonus_client import BonusClient
from entities.backoffice.players.player_bonuses_list import \
    PlayerCurrentBonusesList
from entities.casino.player_bonuses_list import PlayerAvailableBonusesList
from utils.logging.logger import StepLogger


class BonusService:
    """
    Serwis do obsługi bonusów gracza przez gracza.
    """

    def __init__(self, context):
        """
        Inicjalizuje serwis bonusów gracza.

        :param context: Obiekt kontekstu zalogowanego gracza.
        """
        self._context = context

    @allure.step("Player get available bonuses")
    def available_bonuses(self, bonus=None):
        """
        Zwraca listę dostępnych dla gracza bonusów.
        :param bonus: Opcjonalny Obiekt bonusu.
        :return: Zwraca listę obiektów dostępnych bonusów bądź obiekt przekazanego bonusu.
        """
        resp = BonusClient.available_bonuses(self._context)
        StepLogger.log_step(f"PLAYER GET AVAILABLE BONUSES: Player {self._context.email}", response=resp)
        if resp.status_code != 200:
            return resp
        bonus_list = PlayerAvailableBonusesList.from_dict(resp.json())
        if bonus:
            player_bonus = next((b for b in bonus_list if b.bonus_definition_id == bonus.id), None)
            if player_bonus is None:
                raise ValueError(f"Bonus {bonus.name} not available for player {self._context.email}")
            return player_bonus
        return bonus_list

    @allure.step("Player get current bonuses")
    def current_bonuses(self, bonus=None):
        """
        Zwraca listę przypisanych graczowi bonusów.
        :param bonus: Opcjonalny Obiekt bonusu.
        :return: Zwraca listę obiektów przypisanych bonusów bądź obiekt przekazanego bonusu jeśli jest przypisany.
        """
        resp = BonusClient.current_bonuses(self._context)
        StepLogger.log_step(f"PLAYER GET CURRENT BONUSES: Player {self._context.email}")
        if resp.status_code != 200:
            return resp
        bonus_list = PlayerCurrentBonusesList.from_dict(resp.json())
        if bonus:
            current_bonus = next((b for b in bonus_list if b.bonus_definition_id == bonus.bonus_definition_id), None)
            if current_bonus is None:
                raise ValueError(f"Bonus {bonus.name} not in player {self._context.email} available list")
        return bonus_list

    @allure.step("Player accept bonus")
    def accept(self, player_bonus):
        """
        Akceptacja warunków wybranego bonusu.

        :param player_bonus: Obiekt bonusu
        """
        payload = {"claimId": player_bonus.claim_id}
        resp = BonusClient.accept(self._context, payload=payload)
        StepLogger.log_step(f"PLAYER ACCEPT BONUS: {self._context.email} → {player_bonus.presentation_name}", response=resp)
        return resp

    @allure.step("Player claim bonus")
    def claim(self, player_bonus):
        """
        Przyjęcie wybranego bonusu.

        :param player_bonus: Obiekt bonusu
        """
        payload = {"claimId": player_bonus.claim_id}
        resp = BonusClient.claim(self._context, payload=payload)
        StepLogger.log_step(f"PLAYER CLAIM BONUS: {self._context.email} → {player_bonus.presentation_name}", response=resp)
        return resp
