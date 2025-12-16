import random
import uuid

import allure
from api.clients.providers_client.provider_one_client import ProviderOneClient
from api.services.providers_services.game_session import GameSession
from faker import Faker
from utils.logging.logger import StepLogger
from utils.mappers.mappers import PROVIDER_ONE_STATUS_MAP

fake = Faker("pl_PL")


class ProviderOneService(GameSession):
    """
    Serwis do obsługi sesji gier PROVIDER ONE gracza.
    """

    def __init__(self, player, game, free_spins_external_id, auto_auth, player_bonus):
        """

        :param player: Obiekt kontekstu zalogowanego gracza.
        :param game: Obiekt gry PROVIDER ONE.
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
            "token": self.init_token,
            "ip": fake.ipv4(),
            "gameId": self.game.provider_id
        }
        resp = ProviderOneClient.authenticate(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER AUTHENTICATE ON GAME: {self.player.email} → {self.game.name}", response=resp)
        self.authenticate_status = PROVIDER_ONE_STATUS_MAP.get(resp.json().get("status"))

    @allure.step("Player get funds on game")
    def get_funds(self):
        """
        Pobiera i aktualizuje dostępne środki na grze.
        """
        payload = {
            "user":
                {"id": self.player.id,
                 "token": self.init_token
                 }
        }
        resp = ProviderOneClient.get_funds(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER GET FUNDS: {self.player.email} → {self.game.name}", response=resp)
        if resp.status_code == 200:
            self.current_balance = resp.json()["funds"]["balance"]
        else:
            self.current_balance = PROVIDER_ONE_STATUS_MAP.get(resp.json().get("status"))
        return resp.json()["funds"]["balance"]

    # STANDARD GAMEPLAY

    @allure.step("Player bet")
    def bet(self, bet_amount, transaction_id=None, round_id=None,
            free_found=False):
        """
        Dokonuje standardowego zakładu.

        :param bet_amount: (int) Wysokość zakładu.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        :param free_found: (bool) Flaga określająca czy runda jest darmowa.
        """
        transaction_id = transaction_id or random.randint(10 ** 15, 10 ** 16 - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "user":
                {"id": self.player.id,
                 "token": self.init_token
                 },
            "amount": bet_amount,
            "gameId": self.game.provider_game_id,
            "roundId": round_id,
            "transactionId": transaction_id,
            "freeRound": free_found
        }
        resp = ProviderOneClient.bet(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER: BET {bet_amount} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    @allure.step("Player win")
    def win(self, win_amount, transaction_id=None, round_id=None, end_round=True):
        """
        Generuje wynik zakładu

        :param win_amount: (int) Wysokość wygranej.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        :param end_round: (bool) Flaga określająca czy runda została zakończona.
        """
        transaction_id = transaction_id or random.randint(10 ** 15, 10 ** 16 - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "user":
                {"id": self.player.id,
                 "token": self.init_token,
                 },
            "round":
                {"endRound": end_round},
            "amount": win_amount,
            "gameId": self.game.provider_game_id,
            "roundId": round_id,
            "transactionId": transaction_id,
        }
        resp = ProviderOneClient.win(context=self, payload=payload)
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

    # WALLET FREE SPIN GAMEPlAY
    @allure.step("Player wallet free spin bet")
    def wallet_free_spin_bet(self, fs_value=1, transaction_id=None, round_id=None):
        """
        Dokonuje zakładu wallet free spin.

        :param fs_value: (int) Wartość free spina.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        """
        transaction_id = transaction_id or random.randint(10 ** (16 - 1), (10 ** 16) - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "user": {
                "id": self.player.id,
                "token": self.init_token
            },
            "amount": fs_value,
            "gameId": self.game.provider_game_id,
            "roundId": round_id,
            "freeRound": False,
            "freeRoundInfo": None,
            "transactionId": transaction_id,
            "walletFreeSpin": True
        }
        resp = ProviderOneClient.bet(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER WALLET FREE SPIN: FS VALUE {fs_value} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    @allure.step("Player wallet free spin win")
    def wallet_free_spin_win(self, win_amount, transaction_id=None, round_id=None):
        """
        Generuje wynik zakładu wallet free spin.

        :param win_amount: (int) Wysokość wygranej free spin.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        """
        transaction_id = transaction_id or random.randint(10 ** (16 - 1), (10 ** 16) - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "type": 5,
            "user": {
                "id": self.player.id,
                "token": self.init_token
            },
            "round": {
                "endRound": True,
                "lastFreeRound": None
            },
            "amount": win_amount,
            "gameId": self.game.provider_game_id,
            "roundId": round_id,
            "freeRoundInfo": None,
            "transactionId": transaction_id
        }
        resp = ProviderOneClient.win(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER WALLET FREE SPIN: WIN {win_amount} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    def wallet_free_spin_round(self, win_amount, fs_value=1):
        """
        Uruchamia zakład wallet free spin oraz generuje wynik tworząc pełną rundę.

        :param fs_value: (int) Wartość free spina.
        :param win_amount: (int) Wysokość wygranej.
        :return: Zwraca wynik rundy wallet free spin i zapisuje w historii
        """
        round_id = str(uuid.uuid4())
        bet = self.wallet_free_spin_bet(fs_value=fs_value, round_id=round_id)
        win = self.wallet_free_spin_win(win_amount=win_amount, round_id=round_id)
        result = {
            "bet": bet.json() if bet.ok else bet,
            "win": win.json() if win.ok else win
        }
        self.history.append(result)
        return result

    # WALLET FREE SPIN GAMEPlAY

    @allure.step("Player provider free spin bet")
    def provider_free_spin_bet(self, fs_value=1, transaction_id=None, round_id=None):
        """
        Dokonuje zakładu provider free spin.

        :param fs_value: (int) Wartość free spina.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        """
        transaction_id = transaction_id or random.randint(10 ** (16 - 1), (10 ** 16) - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "user": {
                "id": self.player.id,
                "token": self.init_token
            },
            "amount": 0.0,
            "gameId": self.game.provider_game_id,
            "roundId": round_id,
            "freeRound": True,
            "freeRoundInfo": {
                "id": self.free_spin_id,
                "txId": "",
                "betAmount": fs_value,
                "campaignId": ""
            },
            "transactionId": transaction_id
        }
        resp = ProviderOneClient.bet(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER PROVIDER FREE SPIN: FS VALUE {fs_value} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    @allure.step("Player provider free spin win")
    def provider_free_spin_win(self, win_amount, transaction_id=None, round_id=None):
        """
        Generuje wynik zakładu provider free spin.

        :param win_amount: (int) Wysokość wygranej free spin.
        :param transaction_id: (int) 16 cyfrowy identyfikator transakcji.
        :param round_id: (uuid) Identyfikator rundy.
        """
        transaction_id = transaction_id or random.randint(10 ** (16 - 1), (10 ** 16) - 1)
        round_id = round_id or str(uuid.uuid4())
        payload = {
            "type": 1,
            "user": {
                "id": self.player.id,
                "token": self.init_token
            },
            "round": {
                "endRound": True,
                "lastFreeRound": True
            },
            "amount": win_amount,
            "gameId": self.game.provider_game_id,
            "roundId": round_id,
            "freeRoundInfo": {
                "id": self.free_spin_id,
                "txId": "",
                "count": 10,
                "campaignId": "",
            },
            "transactionId": transaction_id
        }
        resp = ProviderOneClient.win(context=self, payload=payload)
        StepLogger.log_step(f"PLAYER PROVIDER FREE SPIN: WIN {win_amount} ON >{self.game.name}<: {self.player.email}", response=resp)
        return resp

    def provider_free_spin_round(self, win_amount, fs_value=1):
        """
        Uruchamia zakład provider free spin oraz generuje wynik tworząc pełną rundę.

        :param fs_value: (int) Wartość free spina.
        :param win_amount: (int) Wysokość wygranej.
        :return: Zwraca wynik rundy wallet free spin i zapisuje w historii
        """
        round_id = str(uuid.uuid4())
        bet = self.provider_free_spin_bet(fs_value=fs_value, round_id=round_id)
        win = self.provider_free_spin_win(win_amount=win_amount, round_id=round_id)
        result = {
            "bet": bet.json() if bet.ok else bet,
            "win": win.json() if win.ok else win
        }
        self.history.append(result)
        return result
