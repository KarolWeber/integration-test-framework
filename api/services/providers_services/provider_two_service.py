import random
import uuid

import allure
from api.clients.providers_client.provider_two_client import ProviderTwoClient
from api.services.providers_services.game_session import GameSession
from faker import Faker
from utils.logging.logger import StepLogger
from utils.mappers.mappers import PROVIDER_TWO_STATUS_MAP

fake = Faker("pl_PL")


class ProviderTwoService(GameSession):
    """
    Serwis do obsługi sesji gier PROVIDER TWO gracza.
    """

    def __init__(self, player, game, free_spins_external_id, auto_auth, player_bonus):
        """

        :param player: Obiekt kontekstu zalogowanego gracza.
        :param game: Obiekt gry PROVIDER TWO.
        :param free_spins_external_id: (uuid, opcjonalny) Identyfikator bonusu free spin przypisany graczowi.
        :param auto_auth: (bool) Flaga ustawiająca automatyczną autentykacji na grze.
        :param player_bonus: Obiekt bonusu gracza.
        """
        super().__init__(player, game, player_bonus)
        self.init_game(free_spins_external_id, player_bonus)
        if auto_auth:
            self.authenticate()

    @allure.step("Player authenticate on game")
    def authenticate(self):
        """
        Autentykuje gracza na grze.
        """
        payload = {
            "args": {
                "caller_id": "bfgames",
                "caller_password": "password",
                "token": self.init_token
            },
            "methodname": "authenticateToken",
            "mirror": {
                "id": "1544602837017426"
            },
            "type": "jsonwsp/request",
            "version": "1.0"
        }

        resp = ProviderTwoClient.authenticate(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER AUTHENTICATE ON GAME: {self.player.email} → {self.game.name}", response=resp)
        self.authenticate_status = PROVIDER_TWO_STATUS_MAP.get(resp.json().get("status"))

    @allure.step("Player get funds on game")
    def get_funds(self):
        """
        Pobiera i aktualizuje dostępne środki na grze.
        """
        payload = {
            "args": {
                "caller_id": "bfgames",
                "caller_password": "password",
                "currency": "PLN",
                "game_ref": self.game.provider_id,
                "token": self.init_token
            },
            "methodname": "getBalance",
            "mirror": {
                "id": "1544603363683526"
            },
            "type": "jsonwsp/request",
            "version": "1.0"
        }
        resp = ProviderTwoClient.get_funds(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER GET FUNDS: {self.player.email} → {self.game.name}", response=resp)
        if resp.status_code == 200:
            self.current_balance = resp.json()["funds"]["balance"]
        else:
            self.current_balance = PROVIDER_TWO_STATUS_MAP.get(resp.json().get("status"))
        return resp.json()["funds"]["balance"]

    # STANDARD GAMEPLAY

    @allure.step("Player bet")
    def bet(self, bet_amount, contribution_amount=0, transaction_id=None, round_id=None,
            free_found=False):
        """
        Dokonuje standardowego zakładu.

        :param bet_amount: (int) Wysokość zakładu.
        :param contribution_amount: (int) Wysokość wkładu do jackpota.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        :param free_found: (bool) Flaga określająca czy runda jest darmowa.
        """
        transaction_id = transaction_id or random.randint(10 ** 15, 10 ** 16 - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "args": {
                "caller_id": "bfgames",
                "caller_password": "password",
                "action_id": transaction_id,
                "amount": bet_amount,
                "currency": "PLN",
                "game_ref": self.game.provider_id,
                "game_ver": "1.0.0",
                "jackpot_contributions": [
                    {
                        "jackpot_id": "mysteryjackpot-bronze",
                        "contribution_amount": contribution_amount
                    }
                ],
                "round_id": round_id,
                "token": self.init_token
            },
            "methodname": "withdraw",
            "mirror": {
                "id": "1544602574783082"
            },
            "type": "jsonwsp/request",
            "version": "1.0"
        }

        resp = ProviderTwoClient.bet(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER: BET {bet_amount} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    @allure.step("Player win")
    def win(self, win_amount, jackpot_win, transaction_id=None, round_id=None, end_round=True):
        """
        Generuje wynik zakładu

        :param win_amount: (int) Wysokość wygranej.
        :param jackpot_win: (int) Wysokość wygranej jackpota.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        :param end_round: (bool) Flaga określająca czy runda została zakończona.
        """
        transaction_id = transaction_id or random.randint(10 ** 15, 10 ** 16 - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "args": {
                "caller_id": "bfgames",
                "caller_password": "password",
                "action_id": transaction_id,
                "round_end": True,
                "amount": win_amount,
                "currency": "PLN",
                "game_ref": self.game.provider_id,
                "game_ver": "1.0.0",
                "jackpot_winnings": [{
                    "jackpot_id": "mysteryjackpot-bronze",
                    "winnings_amount": jackpot_win
                }],
                "offline": False,
                "round_id": round_id,
                "token": self.init_token
            },
            "methodname": "deposit",
            "mirror": {
                "id": "1544602607201120"
            },
            "type": "jsonwsp/request",
            "version": "1.0"
        }

        resp = ProviderTwoClient.win(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER: WIN {win_amount} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    def round(self, bet_amount, win_amount):
        """
        Uruchamia zakład oraz generuje wynik tworząc pełną rundę.

        :param bet_amount: (int) Wysokość zakładu.
        :param win_amount: (int) Wysokość wygranej.
        :return: Zwraca wynik rundy i zapisuje w historii
        """
        round_id = str(uuid.uuid4())
        bet = self.bet(bet_amount=bet_amount, round_id=round_id)
        win = self.win(win_amount=win_amount, round_id=round_id)
        result = {
            "bet": bet.json() if bet.ok else bet,
            "win": win.json() if win.ok else win
        }
        self.history.append(result)
        return result
